-- Create the payments table to store payment history
CREATE TABLE IF NOT EXISTS public.payments (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  stripe_checkout_id TEXT,
  amount INTEGER NOT NULL,
  -- Amount in cents
  currency TEXT NOT NULL,
  status TEXT NOT NULL,
  payment_type TEXT NOT NULL,
  -- 'one-time' or 'subscription'
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);
-- Set up RLS (Row Level Security) policies
ALTER TABLE public.payments ENABLE ROW LEVEL SECURITY;
-- Policy to allow users to read only their own payment history
CREATE POLICY "Users can view their own payment history" ON public.payments FOR
SELECT USING (auth.uid() = user_id);
-- Policy for server-side functions to create payment records
CREATE POLICY "Server can insert payment records" ON public.payments FOR
INSERT TO authenticated WITH CHECK (true);
-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_payments_user_id ON public.payments(user_id);
CREATE INDEX IF NOT EXISTS idx_payments_stripe_checkout_id ON public.payments(stripe_checkout_id);
-- Comments for documentation
COMMENT ON TABLE public.payments IS 'Stores payment history information';
COMMENT ON COLUMN public.payments.user_id IS 'References the user in auth.users';
COMMENT ON COLUMN public.payments.stripe_checkout_id IS 'Stripe checkout session ID';
COMMENT ON COLUMN public.payments.amount IS 'Payment amount in cents';
COMMENT ON COLUMN public.payments.status IS 'Payment status (succeeded, failed, etc.)';
COMMENT ON COLUMN public.payments.payment_type IS 'Type of payment (one-time or subscription)';