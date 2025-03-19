-- Create the subscriptions table
CREATE TABLE IF NOT EXISTS public.subscriptions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  stripe_customer_id TEXT,
  stripe_subscription_id TEXT,
  status TEXT NOT NULL,
  price_id TEXT,
  quantity INTEGER NOT NULL DEFAULT 1,
  cancel_at_period_end BOOLEAN NOT NULL DEFAULT FALSE,
  current_period_start TIMESTAMP WITH TIME ZONE,
  current_period_end TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE
);
-- Set up RLS (Row Level Security) policies
ALTER TABLE public.subscriptions ENABLE ROW LEVEL SECURITY;
-- Policy to allow users to read only their own subscriptions
CREATE POLICY "Users can view their own subscriptions" ON public.subscriptions FOR
SELECT USING (auth.uid() = user_id);
-- Policy to allow authenticated users to create subscriptions (will be limited in function)
CREATE POLICY "Users can create their own subscriptions" ON public.subscriptions FOR
INSERT WITH CHECK (auth.uid() = user_id);
-- Policy to allow authenticated users to update their own subscriptions
CREATE POLICY "Users can update their own subscriptions" ON public.subscriptions FOR
UPDATE USING (auth.uid() = user_id);
-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_subscriptions_user_id ON public.subscriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_stripe_subscription_id ON public.subscriptions(stripe_subscription_id);
-- Comments for documentation
COMMENT ON TABLE public.subscriptions IS 'Stores Stripe subscription information for users';
COMMENT ON COLUMN public.subscriptions.user_id IS 'References the user in auth.users';
COMMENT ON COLUMN public.subscriptions.stripe_customer_id IS 'Stripe customer ID for the user';
COMMENT ON COLUMN public.subscriptions.stripe_subscription_id IS 'Stripe subscription ID';
COMMENT ON COLUMN public.subscriptions.status IS 'Subscription status (active, canceled, etc.)';
COMMENT ON COLUMN public.subscriptions.current_period_end IS 'When the current subscription period ends';