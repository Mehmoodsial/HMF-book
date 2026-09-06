import 'package:flutter/material.dart';

class SignUpScreen extends StatefulWidget {
  const SignUpScreen({super.key});

  @override
  State<SignUpScreen> createState() => _SignUpScreenState();
}

class _SignUpScreenState extends State<SignUpScreen> {
  final _formKey = GlobalKey<FormState>();
  final _usernameController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _obscurePassword = true;

  @override
  void dispose() {
    _usernameController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SingleChildScrollView(
        child: Column(
          children: [
            // ---- Green header with HMF ----
            Container(
              width: double.infinity,
              height: 160,
              decoration: const BoxDecoration(
                gradient: LinearGradient(
                  colors: [Color(0xFF43A047), Color(0xFF2E7D32)],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                borderRadius: BorderRadius.only(
                  bottomLeft: Radius.circular(40),
                  bottomRight: Radius.circular(40),
                ),
              ),
              child: const Center(
                child: Text(
                  'HMF',
                  style: TextStyle(
                    fontSize: 42,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                    letterSpacing: 3,
                  ),
                ),
              ),
            ),

            const SizedBox(height: 30),

            // ---- Title ----
            const Text(
              'Create Account',
              style: TextStyle(
                fontSize: 26,
                fontWeight: FontWeight.bold,
                color: Colors.black87,
              ),
            ),
            const SizedBox(height: 6),
            const Text(
              'Sign up to get started',
              style: TextStyle(fontSize: 14, color: Colors.grey),
            ),

            const SizedBox(height: 30),

            // ---- Input fields ----
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 25),
              child: Form(
                key: _formKey,
                child: Column(
                  children: [
                    _buildTextField(
                      controller: _usernameController,
                      hint: 'Username',
                      icon: Icons.person_outline,
                    ),
                    const SizedBox(height: 16),
                    _buildTextField(
                      controller: _emailController,
                      hint: 'Email',
                      icon: Icons.email_outlined,
                      keyboardType: TextInputType.emailAddress,
                    ),
                    const SizedBox(height: 16),
                    _buildTextField(
                      controller: _passwordController,
                      hint: 'Password',
                      icon: Icons.lock_outline,
                      isPassword: true,
                    ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 30),

            // ---- Sign Up Button ----
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 25),
              child: SizedBox(
                width: double.infinity,
                height: 55,
                child: ElevatedButton(
                  onPressed: () {
                    if (_formKey.currentState!.validate()) {
                      // Yahan aap signup ki logic likhein (Firebase etc.)
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text('Account created!')),
                      );
                    }
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF2E7D32),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(30),
                    ),
                    elevation: 4,
                  ),
                  child: const Text(
                    'Sign Up',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.w600,
                      color: Colors.white,
                    ),
                  ),
                ),
              ),
            ),

            const SizedBox(height: 30),

            // ---- Or continue with ----
            const Text(
              'Or continue with',
              style: TextStyle(color: Colors.grey, fontSize: 14),
            ),

            const SizedBox(height: 20),

            // ---- Social buttons (Google, Snapchat, Facebook) ----
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                _socialButton('G', const Color(0xFFDB4437)),
                const SizedBox(width: 20),
                _socialButton('S', const Color(0xFFFFFC00)),
                const SizedBox(width: 20),
                _socialButton('f', const Color(0xFF4267B2)),
              ],
            ),

            const SizedBox(height: 30),

            // ---- Login link ----
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Text("Already have an account? "),
                GestureDetector(
                  onTap: () {
                    // Yahan login page ka route lagayein
                  },
                  child: const Text(
                    'Login',
                    style: TextStyle(
                      color: Color(0xFF2E7D32),
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),

            const SizedBox(height: 30),
          ],
        ),
      ),
    );
  }

  Widget _buildTextField({
    required TextEditingController controller,
    required String hint,
    required IconData icon,
    bool isPassword = false,
    TextInputType keyboardType = TextInputType.text,
  }) {
    return TextFormField(
      controller: controller,
      obscureText: isPassword ? _obscurePassword : false,
      keyboardType: keyboardType,
      decoration: InputDecoration(
        hintText: hint,
        prefixIcon: Icon(icon, color: Colors.grey),
        suffixIcon: isPassword
            ? IconButton(
                icon: Icon(
                  _obscurePassword ? Icons.visibility_off : Icons.visibility,
                  color: Colors.grey,
                ),
                onPressed: () {
                  setState(() {
                    _obscurePassword = !_obscurePassword;
                  });
                },
              )
            : null,
        filled: true,
        fillColor: Colors.grey.shade100,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(15),
          borderSide: BorderSide.none,
        ),
      ),
      validator: (value) {
        if (value == null || value.isEmpty) {
          return 'Please enter $hint';
        }
        return null;
      },
    );
  }

  Widget _socialButton(String label, Color color) {
    return GestureDetector(
      onTap: () {
        // Social login logic yahan likhein
      },
      child: CircleAvatar(
        radius: 28,
        backgroundColor: color,
        child: Text(
          label,
          style: TextStyle(
            fontSize: 22,
            fontWeight: FontWeight.bold,
            color: color == const Color(0xFFFFFC00) ? Colors.black : Colors.white,
          ),
        ),
      ),
    );
  }
}
