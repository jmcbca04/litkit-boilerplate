# LitKit Authentication Module

This module provides authentication functionality for LitKit applications using Supabase.

## Current Status: Demo/Scaffolding Mode

The authentication module is currently in **scaffolding mode**, meaning:

- The code structure and patterns are in place
- All functions work in "demo mode" (no actual Supabase connection)
- Users can see how authentication would function
- No real authentication is happening yet

## How to Enable Real Authentication

To enable real authentication with Supabase:

1. Create a Supabase project at [https://supabase.com](https://supabase.com)
2. Get your project URL and anon key from the Supabase dashboard
3. Add these credentials to your `.env` file:
   ```
   SUPABASE_URL=your-project-url
   SUPABASE_KEY=your-anon-key
   ```
4. Uncomment the actual function calls in the auth.py file:

   ```python
   # Before (demo mode):
   # data = supabase_client.auth.sign_up({"email": email, "password": password})

   # After (real authentication):
   data = supabase_client.auth.sign_up({"email": email, "password": password})
   ```

5. Configure your Supabase project's authentication settings:
   - Set site URL to your application URL
   - Configure redirect URLs
   - Set up social login providers if needed

## File Structure

- `__init__.py` - Package initialization
- `client.py` - Supabase client configuration
- `auth.py` - Authentication functions (login, signup, etc.)

## Usage Examples

See the example applications in the `examples/` directory:

- `auth_example.py` - Full authentication flow
- `private_page_example.py` - Protected content example

## Additional Resources

- [Supabase Authentication Documentation](https://supabase.com/docs/guides/auth)
- [LitKit Auth Guide](../../docs/supabase_auth_guide.md)
