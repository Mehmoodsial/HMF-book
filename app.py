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
    final screenHeight = MediaQuery.of(context).size.height;

    return Scaffold(
      body: Container(
        width: double.infinity,
        height: double.infinity,
        // Premium Green Gradient Theme
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [
              Color(0xFF00B074), // Light Green
              Color(0xFF056839), // Dark Green
            ],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: SafeArea(
          bottom: false,
          child: Column(
            children: [
              // Top Header HMF Logo (25% Height)
              SizedBox(
                height: screenHeight * 0.25,
                child: const Center(
                  child: Text(
                    'HMF',
                    style: TextStyle(
                      fontSize: 64,
                      fontWeight: FontWeight.w900,
                      color: Colors.white,
                      letterSpacing: 1.5,
                    ),
                  ),
                ),
              ),

              // Main Input White Sheet Card (75% Height)
              Expanded(
                child: Container(
                  width: double.infinity,
                  decoration: const BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.only(
                      topLeft: Radius.circular(40),
                      topRight: Radius.circular(40),
                    ),
                  ),
                  child: SingleChildScrollView(
                    physics: const BouncingScrollPhysics(),
                    padding: const EdgeInsets.symmetric(horizontal: 28, vertical: 32),
                    child: Form(
                      key: _formKey,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'Create Account',
                            style: TextStyle(
                              fontSize: 26,
                              fontWeight: FontWeight.bold,
                              color: Color(0xFF2D3142),
                            ),
                          ),
                          
                          const SizedBox(height: 24),

                          // Username Field
                          _buildTextField(
                            controller: _usernameController,
                            hint: 'Username',
                            icon: Icons.person_outline_rounded,
                          ),
                          
                          const SizedBox(height: 16),

                          // Email Field
                          _buildTextField(
                            controller: _emailController,
                            hint: 'Email',
                            icon: Icons.mail_outline_rounded,
                            keyboardType: TextInputType.emailAddress,
                          ),
                          
                          const SizedBox(height: 16),

                          // Password Field
                          _buildTextField(
                            controller: _passwordController,
                            hint: 'Password',
                            icon: Icons.lock_outline_rounded,
                            isPassword: true,
                          ),

                          const SizedBox(height: 32),

                          // Sign Up Action Button
                          SizedBox(
                            width: double.infinity,
                            height: 54,
                            child: ElevatedButton(
                              onPressed: () {
                                if (_formKey.currentState!.validate()) {
                                  ScaffoldMessenger.of(context).showSnackBar(
                                    const SnackBar(content: Text('Creating HMF Account...')),
                                  );
                                }
                              },
                              style: ElevatedButton.styleFrom(
                                backgroundColor: const Color(0xFF00A86B),
                                foregroundColor: Colors.white,
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(28),
                                ),
                              ),
                              child: const Text(
                                'Sign Up',
                                style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                              ),
                            ),
                          ),

                          const SizedBox(height: 28),

                          // Divider Line
                          Row(
                            children: const [
                              Expanded(child: Divider(color: Color(0xFFE2E8F0), thickness: 1)),
                              Padding(
                                padding: EdgeInsets.symmetric(horizontal: 16),
                                child: Text('Or continue with', style: TextStyle(color: Colors.grey, fontSize: 13)),
                              ),
                              Expanded(child: Divider(color: Color(0xFFE2E8F0), thickness: 1)),
                            ],
                          ),

                          const SizedBox(height: 20),

                          // Spherical Social Icons
                          Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              _socialButton('G', const Color(0xFFEA4335), Colors.white),
                              const SizedBox(width: 20),
                              _socialButton('S', const Color(0xFFFFFC00), Colors.black),
                              const SizedBox(width: 20),
                              _socialButton('f', const Color(0xFF1877F2), Colors.white),
                            ],
                          ),

                          const SizedBox(height: 32),

                          // Bottom Switch Route Option
                          Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              const Text("Already have an account? ", style: TextStyle(color: Colors.grey, fontSize: 14)),
                              GestureDetector(
                                onTap: () {},
                                child: const Text(
                                  'Login',
                                  style: TextStyle(color: Color(0xFF00A86B), fontWeight: FontWeight.bold, fontSize: 14),
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
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
        prefixIcon: Icon(icon, color: Colors.grey.shade400, size: 22),
        suffixIcon: isPassword
            ? IconButton(
                icon: Icon(_obscurePassword ? Icons.visibility_off_outlined : Icons.visibility_outlined, color: Colors.grey.shade400, size: 20),
                onPressed: () => setState(() => _obscurePassword = !_obscurePassword),
              )
            : null,
        contentPadding: const EdgeInsets.symmetric(vertical: 18, horizontal: 16),
        filled: true,
        fillColor: Colors.white,
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(color: Colors.grey.shade300),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: Color(0xFF00A86B), width: 1.5),
        ),
      ),
      validator: (value) => value == null || value.isEmpty ? 'Please enter $hint' : null,
    );
  }

  Widget _socialButton(String label, Color bgColors, Color textColors) {
    return Container(
      width: 48,
      height: 48,
      decoration: BoxDecoration(color: bgColors, shape: BoxShape.circle),
      child: Center(
        child: Text(
          label,
          style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: textColors, fontFamily: label == 'f' ? 'Georgia' : 'sans-serif'),
        ),
      ),
    );
  }
}
