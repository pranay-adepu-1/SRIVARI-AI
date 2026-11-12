import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import '../providers/language_provider.dart';
import '../services/storage_service.dart';
import '../utils/theme.dart';
import '../utils/constants.dart';
import 'home_dashboard_screen.dart';

class OnboardingScreen extends StatefulWidget {
  const OnboardingScreen({super.key});

  @override
  State<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends State<OnboardingScreen> {
  final PageController _pageController = PageController();
  int _currentPage = 0;

  final List<Map<String, dynamic>> _slides = [
    {
      "icon": Icons.psychology,
      "title_te": "శ్రీవారి AI సహాయకుడు",
      "title_en": "Intelligent Devotee Assistant",
      "desc_te": "దర్శనం, సేవలు, గదులు మరియు నియమాలపై మీ సందేహాలను తెలుగు మరియు ఇంగ్లీషులో ఎప్పుడైనా అడగండి.",
      "desc_en": "Ask anything about Tirumala Darshan, Srivari Seva, cottages, and rules in English or Telugu anytime.",
    },
    {
      "icon": Icons.notifications_active,
      "title_te": "కోటా విడుదల హెచ్చరికలు",
      "title_en": "Real-time Quota Releases",
      "desc_te": "రూ. 300 ప్రత్యేక ప్రవేశ దర్శనం, శ్రీవారి సేవ మరియు వసతి ఆన్‌లైన్ కోటా విడుదల కాగానే తక్షణ నోటిఫికేషన్లు పొందండి.",
      "desc_en": "Get notified the moment ₹300 SED, Srivari Seva, or accommodation online quotas open on official portals.",
    },
    {
      "icon": Icons.verified,
      "title_te": "అధికారిక టీటీడీ సమాచారం",
      "title_en": "Verified Official Information",
      "desc_te": "అన్ని వివరాలు కేవలం news.tirumala.org మరియు ttdevasthanams.ap.gov.in నుండి ధృవీకరించబడినవి మాత్రమే.",
      "desc_en": "All answers are strictly cited and retrieved directly from official TTD channels without intermediaries.",
    },
  ];

  Future<void> _completeOnboarding() async {
    final storage = StorageService();
    await storage.setOnboardingDone(true);
    if (!mounted) return;
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (_) => const HomeDashboardScreen()),
    );
  }

  @override
  Widget build(BuildContext context) {
    final langProvider = Provider.of<LanguageProvider>(context);
    final isTe = langProvider.isTelugu;

    return Scaffold(
      backgroundColor: AppTheme.creamBg,
      body: SafeArea(
        child: Column(
          children: [
            // Top Language Switcher Bar
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    "॥ శ్రీః ॥",
                    style: GoogleFonts.cinzel(
                      color: AppTheme.maroonPrimary,
                      fontWeight: FontWeight.bold,
                      fontSize: 18,
                    ),
                  ),
                  Row(
                    children: [
                      _langChip("తెలుగు", isTe, () => langProvider.setLanguage('te')),
                      const SizedBox(width: 8),
                      _langChip("English", !isTe, () => langProvider.setLanguage('en')),
                    ],
                  )
                ],
              ),
            ),

            // Page Carousel
            Expanded(
              child: PageView.builder(
                controller: _pageController,
                itemCount: _slides.length,
                onPageChanged: (index) {
                  setState(() => _currentPage = index);
                },
                itemBuilder: (context, index) {
                  final slide = _slides[index];
                  return Padding(
                    padding: const EdgeInsets.all(28.0),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Container(
                          width: 110,
                          height: 110,
                          decoration: BoxDecoration(
                            color: AppTheme.maroonPrimary.withOpacity(0.08),
                            shape: BoxShape.circle,
                            border: Border.all(color: AppTheme.goldPrimary, width: 2),
                          ),
                          child: Icon(
                            slide['icon'] as IconData,
                            size: 52,
                            color: AppTheme.maroonPrimary,
                          ),
                        ),
                        const SizedBox(height: 32),
                        Text(
                          isTe ? slide['title_te'] : slide['title_en'],
                          style: GoogleFonts.cinzel(
                            fontSize: 22,
                            fontWeight: FontWeight.bold,
                            color: AppTheme.maroonPrimary,
                          ),
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 14),
                        Text(
                          isTe ? slide['desc_te'] : slide['desc_en'],
                          style: GoogleFonts.plusJakartaSans(
                            fontSize: 14,
                            color: AppTheme.textMuted,
                            height: 1.5,
                          ),
                          textAlign: TextAlign.center,
                        ),
                      ],
                    ),
                  );
                },
              ),
            ),

            // Indicator Dots
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: List.generate(
                _slides.length,
                (i) => Container(
                  width: _currentPage == i ? 22 : 8,
                  height: 8,
                  margin: const EdgeInsets.symmetric(horizontal: 4),
                  decoration: BoxDecoration(
                    color: _currentPage == i ? AppTheme.maroonPrimary : AppTheme.borderLight,
                    borderRadius: BorderRadius.circular(4),
                  ),
                ),
              ),
            ),

            const SizedBox(height: 24),

            // Disclaimer Notice
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24.0),
              child: Text(
                isTe
                    ? "గమనిక: శ్రీవారి AI అనేది స్వతంత్ర సమాచార వేదిక. టికెట్లు మరియు సేవల బుకింగ్ ttdevasthanams.ap.gov.in ద్వారా మాత్రమే జరుగుతుంది."
                    : "Note: Srivari AI is an independent informational guide. All bookings are completed exclusively on ttdevasthanams.ap.gov.in.",
                style: const TextStyle(fontSize: 11, color: AppTheme.textMuted),
                textAlign: TextAlign.center,
              ),
            ),

            const SizedBox(height: 20),

            // Next / Get Started Button
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 12),
              child: SizedBox(
                width: double.infinity,
                height: 52,
                child: ElevatedButton(
                  onPressed: () {
                    if (_currentPage < _slides.length - 1) {
                      _pageController.nextPage(
                        duration: const Duration(milliseconds: 300),
                        curve: Curves.easeInOut,
                      );
                    } else {
                      _completeOnboarding();
                    }
                  },
                  child: Text(
                    _currentPage < _slides.length - 1
                        ? (isTe ? "తరువాత" : "Next")
                        : (isTe ? "ప్రారంభించండి (Start)" : "Get Started"),
                    style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 12),
          ],
        ),
      ),
    );
  }

  Widget _langChip(String label, bool isSelected, VoidCallback onTap) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(20),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
        decoration: BoxDecoration(
          color: isSelected ? AppTheme.maroonPrimary : Colors.white,
          border: Border.all(color: AppTheme.goldPrimary),
          borderRadius: BorderRadius.circular(20),
        ),
        child: Text(
          label,
          style: TextStyle(
            color: isSelected ? Colors.white : AppTheme.textDark,
            fontWeight: FontWeight.bold,
            fontSize: 12,
          ),
        ),
      ),
    );
  }
}

