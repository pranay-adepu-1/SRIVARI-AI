import 'dart:async';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import '../providers/auth_provider.dart';
import '../providers/language_provider.dart';
import '../services/storage_service.dart';
import '../utils/theme.dart';
import 'onboarding_screen.dart';
import 'home_dashboard_screen.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> with SingleTickerProviderStateMixin {
  late AnimationController _animController;
  late Animation<double> _scaleAnimation;
  late Animation<double> _fadeAnimation;

  @override
  void initState() {
    super.initState();
    _animController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1800),
    );

    _scaleAnimation = Tween<double>(begin: 0.85, end: 1.0).animate(
      CurvedAnimation(parent: _animController, curve: Curves.easeOutBack),
    );

    _fadeAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _animController, curve: Curves.easeIn),
    );

    _animController.forward();
    _navigateNext();
  }

  Future<void> _navigateNext() async {
    final storage = StorageService();
    final langProvider = Provider.of<LanguageProvider>(context, listen: false);
    final authProvider = Provider.of<AuthProvider>(context, listen: false);

    // Initialize auth in parallel
    authProvider.initAuth(langProvider.currentLanguage);

    await Future.delayed(const Duration(milliseconds: 2400));
    final isOnboarded = await storage.isOnboardingDone();

    if (!mounted) return;
    if (isOnboarded) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (_) => const HomeDashboardScreen()),
      );
    } else {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (_) => const OnboardingScreen()),
      );
    }
  }

  @override
  void dispose() {
    _animController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        width: double.infinity,
        decoration: const BoxDecoration(
          gradient: RadialGradient(
            center: Alignment(0, -0.2),
            radius: 1.2,
            colors: [
              Color(0xFF8B0000), // Deep sacred crimson
              Color(0xFF4A0000),
              Color(0xFF260000),
            ],
          ),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Spacer(),
            ScaleTransition(
              scale: _scaleAnimation,
              child: FadeTransition(
                fade: _fadeAnimation,
                child: Column(
                  children: [
                    // Divine Namam / Temple Icon Emblem
                    Container(
                      width: 110,
                      height: 110,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: AppTheme.maroonDeep,
                        border: Border.all(color: AppTheme.goldPrimary, width: 2.5),
                        boxShadow: [
                          BoxShadow(
                            color: AppTheme.goldPrimary.withOpacity(0.35),
                            blurRadius: 24,
                            spreadRadius: 4,
                          ),
                        ],
                      ),
                      child: const Center(
                        child: Icon(
                          Icons.temple_hindu,
                          size: 58,
                          color: AppTheme.goldLight,
                        ),
                      ),
                    ),
                    const SizedBox(height: 28),
                    Text(
                      "॥ ॐ నమో వేంకటేశాయ ॥",
                      style: GoogleFonts.cinzel(
                        fontSize: 16,
                        fontWeight: FontWeight.w700,
                        color: AppTheme.goldLight,
                        letterSpacing: 2,
                      ),
                    ),
                    const SizedBox(height: 10),
                    Text(
                      "శ్రీవారి AI",
                      style: GoogleFonts.cinzel(
                        fontSize: 34,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    Text(
                      "Srivari AI",
                      style: GoogleFonts.cinzel(
                        fontSize: 20,
                        fontWeight: FontWeight.w600,
                        color: AppTheme.goldLight,
                        letterSpacing: 1.5,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      "Your Intelligent Tirumala Assistant",
                      style: GoogleFonts.plusJakartaSans(
                        fontSize: 13,
                        color: Colors.white70,
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const Spacer(),
            const CircularProgressIndicator(
              color: AppTheme.goldPrimary,
              strokeWidth: 2.5,
            ),
            const SizedBox(height: 16),
            Text(
              "Independent Devotional Assistant",
              style: GoogleFonts.plusJakartaSans(
                fontSize: 11,
                color: Colors.white54,
              ),
            ),
            const SizedBox(height: 36),
          ],
        ),
      ),
    );
  }
}

