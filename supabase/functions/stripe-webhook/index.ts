// Supabase Edge Function for handling Stripe webhooks
import { serve } from 'https://deno.land/std@0.188.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'
import Stripe from 'https://esm.sh/stripe@12.18.0'

// Initialize Stripe with API key from environment
const stripe = new Stripe(Deno.env.get('STRIPE_API_KEY') || '', {
  apiVersion: '2023-10-16',
  httpClient: Stripe.createFetchHttpClient(),
})

// This is needed for signature verification
const cryptoProvider = Stripe.createSubtleCryptoProvider()

// Handle the HTTP request
serve(async (request: Request) => {
  try {
    // Get the signature from the header
    const signature = request.headers.get('Stripe-Signature')
    
    if (!signature) {
      return new Response('Missing Stripe signature', { status: 400 })
    }

    // Get the raw body as text
    const body = await request.text()
    
    // Verify the signature
    let event
    try {
      event = await stripe.webhooks.constructEventAsync(
        body,
        signature,
        Deno.env.get('STRIPE_WEBHOOK_SECRET') || '',
        undefined,
        cryptoProvider
      )
    } catch (err) {
      console.error(`Webhook signature verification failed: ${err.message}`)
      return new Response(`Webhook signature verification failed: ${err.message}`, { status: 400 })
    }

    // Initialize Supabase client
    const supabaseUrl = Deno.env.get('SUPABASE_URL') || ''
    const supabaseKey = Deno.env.get('SUPABASE_ANON_KEY') || ''
    const supabase = createClient(supabaseUrl, supabaseKey)

    console.log(`Processing webhook event: ${event.type}`)

    // Handle different event types
    switch (event.type) {
      case 'checkout.session.completed': {
        const session = event.data.object as Stripe.Checkout.Session
        
        // Get the customer email
        const customerEmail = session.customer_email
        if (!customerEmail) {
          console.error('No customer email in session')
          return new Response('No customer email in session', { status: 400 })
        }

        console.log(`Checkout completed for customer: ${customerEmail}`)
        
        // Find the user ID for this email
        const { data: userData, error: userError } = await supabase
          .from('users')
          .select('id')
          .eq('email', customerEmail)
          .single()
        
        if (userError || !userData) {
          console.error(`Error finding user: ${userError?.message || 'User not found'}`)
          return new Response('User not found', { status: 404 })
        }
        
        const userId = userData.id
        
        // Handle one-time payment
        if (session.mode === 'payment') {
          // Create payment record
          const { error: paymentError } = await supabase
            .from('payments')
            .insert({
              user_id: userId,
              stripe_checkout_id: session.id,
              amount: session.amount_total,
              currency: session.currency,
              status: 'succeeded',
              payment_type: 'one-time'
            })
          
          if (paymentError) {
            console.error(`Error creating payment record: ${paymentError.message}`)
            return new Response('Error creating payment record', { status: 500 })
          }
          
          // Handle credits if applicable
          if (session.amount_total) {
            // Calculate credits (example: 1 credit per $1)
            const creditAmount = Math.floor(session.amount_total / 100)
            
            // Get current credits
            const { data: creditData, error: creditError } = await supabase
              .from('credits')
              .select('amount')
              .eq('user_id', userId)
              .single()
            
            const currentCredits = creditData?.amount || 0
            const newCredits = currentCredits + creditAmount
            
            // Update or insert credits
            if (creditData) {
              // Update existing record
              const { error: updateError } = await supabase
                .from('credits')
                .update({ amount: newCredits, updated_at: new Date().toISOString() })
                .eq('user_id', userId)
              
              if (updateError) {
                console.error(`Error updating credits: ${updateError.message}`)
                return new Response('Error updating credits', { status: 500 })
              }
            } else {
              // Insert new record
              const { error: insertError } = await supabase
                .from('credits')
                .insert({
                  user_id: userId,
                  amount: creditAmount,
                  created_at: new Date().toISOString(),
                  updated_at: new Date().toISOString()
                })
              
              if (insertError) {
                console.error(`Error inserting credits: ${insertError.message}`)
                return new Response('Error inserting credits', { status: 500 })
              }
            }
            
            console.log(`Added ${creditAmount} credits for user ${userId}`)
          }
        }
        // Handle subscription
        else if (session.mode === 'subscription') {
          // If subscription was created, it will be in the subscription field
          if (session.subscription) {
            // Retrieve the subscription details
            const subscriptionId = typeof session.subscription === 'string' 
              ? session.subscription 
              : session.subscription.id
            
            const subscription = await stripe.subscriptions.retrieve(subscriptionId)
            
            // Create or update subscription record
            const { error: subscriptionError } = await supabase
              .from('subscriptions')
              .insert({
                user_id: userId,
                stripe_customer_id: session.customer,
                stripe_subscription_id: subscriptionId,
                status: subscription.status,
                price_id: subscription.items.data[0]?.price.id,
                current_period_start: new Date(subscription.current_period_start * 1000).toISOString(),
                current_period_end: new Date(subscription.current_period_end * 1000).toISOString(),
                created_at: new Date().toISOString(),
                updated_at: new Date().toISOString()
              })
            
            if (subscriptionError) {
              console.error(`Error creating subscription record: ${subscriptionError.message}`)
              return new Response('Error creating subscription record', { status: 500 })
            }
            
            console.log(`Created subscription record for user ${userId}`)
          }
        }
        
        break
      }
      
      case 'invoice.payment_succeeded': {
        const invoice = event.data.object as Stripe.Invoice
        
        // Only handle subscription invoices
        if (invoice.subscription) {
          const subscriptionId = typeof invoice.subscription === 'string'
            ? invoice.subscription
            : invoice.subscription.id
          
          // Get the subscription
          const subscription = await stripe.subscriptions.retrieve(subscriptionId)
          
          // Find the subscription in our database
          const { data: subscriptionData, error: subError } = await supabase
            .from('subscriptions')
            .select('user_id')
            .eq('stripe_subscription_id', subscriptionId)
            .single()
          
          if (subError || !subscriptionData) {
            console.error(`Error finding subscription: ${subError?.message || 'Subscription not found'}`)
            return new Response('Subscription not found', { status: 404 })
          }
          
          const userId = subscriptionData.user_id
          
          // Update the subscription
          const { error: updateError } = await supabase
            .from('subscriptions')
            .update({
              status: subscription.status,
              current_period_start: new Date(subscription.current_period_start * 1000).toISOString(),
              current_period_end: new Date(subscription.current_period_end * 1000).toISOString(),
              updated_at: new Date().toISOString()
            })
            .eq('stripe_subscription_id', subscriptionId)
          
          if (updateError) {
            console.error(`Error updating subscription: ${updateError.message}`)
            return new Response('Error updating subscription', { status: 500 })
          }
          
          console.log(`Updated subscription ${subscriptionId} for user ${userId}`)
          
          // Create payment record
          const { error: paymentError } = await supabase
            .from('payments')
            .insert({
              user_id: userId,
              stripe_checkout_id: invoice.id,
              amount: invoice.amount_paid,
              currency: invoice.currency,
              status: 'succeeded',
              payment_type: 'subscription'
            })
          
          if (paymentError) {
            console.error(`Error creating payment record: ${paymentError.message}`)
            return new Response('Error creating payment record', { status: 500 })
          }
        }
        
        break
      }
      
      case 'customer.subscription.updated': {
        const subscription = event.data.object as Stripe.Subscription
        
        // Find the subscription in our database
        const { data: subscriptionData, error: subError } = await supabase
          .from('subscriptions')
          .select('user_id')
          .eq('stripe_subscription_id', subscription.id)
          .single()
        
        if (subError || !subscriptionData) {
          console.error(`Error finding subscription: ${subError?.message || 'Subscription not found'}`)
          return new Response('Subscription not found', { status: 404 })
        }
        
        // Update the subscription
        const { error: updateError } = await supabase
          .from('subscriptions')
          .update({
            status: subscription.status,
            cancel_at_period_end: subscription.cancel_at_period_end,
            current_period_end: new Date(subscription.current_period_end * 1000).toISOString(),
            updated_at: new Date().toISOString()
          })
          .eq('stripe_subscription_id', subscription.id)
        
        if (updateError) {
          console.error(`Error updating subscription: ${updateError.message}`)
          return new Response('Error updating subscription', { status: 500 })
        }
        
        console.log(`Updated subscription ${subscription.id} with status ${subscription.status}`)
        
        break
      }
      
      case 'customer.subscription.deleted': {
        const subscription = event.data.object as Stripe.Subscription
        
        // Update the subscription status to canceled
        const { error: updateError } = await supabase
          .from('subscriptions')
          .update({
            status: 'canceled',
            updated_at: new Date().toISOString()
          })
          .eq('stripe_subscription_id', subscription.id)
        
        if (updateError) {
          console.error(`Error updating subscription: ${updateError.message}`)
          return new Response('Error updating subscription', { status: 500 })
        }
        
        console.log(`Marked subscription ${subscription.id} as canceled`)
        
        break
      }
    }
    
    // Return a success response
    return new Response(JSON.stringify({ received: true }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    })
  } catch (err) {
    // Handle any unexpected errors
    console.error(`Webhook error: ${err.message}`)
    return new Response(`Webhook error: ${err.message}`, { status: 500 })
  }
}) 