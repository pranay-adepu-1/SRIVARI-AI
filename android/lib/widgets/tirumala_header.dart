import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../utils/theme.dart';
import 'language_switch_button.dart';

class TirumalaHeader extends StatelessWidget {
  final String title;
  final String subtitle;
  final bool showLanguageSwitch;

  const TirumalaHeader({
    super.key,
    required this.title,
    required this.subtitle,
    this.showLanguageSwitch = true,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      decoration: const BoxDecoration(
        gradient: LinearGradient(
          colors: [AppTheme.maroonDeep, AppTheme.maroonPrimary],
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black26,
            blurRadius: 8,
            offset: Offset(0, 4),
          )
        ],
      ),
      padding: EdgeInsets.only(
        top: MediaQuery.of(context).padding.top + 12,
        bottom: 20,
        left: 20,
        right: 20,
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                "॥ ॐ నమో వేంకటేశాయ ॥",
                style: GoogleFonts.cinzel(
                  color: AppTheme.goldLight,
                  fontSize: 13,
                  fontWeight: FontWeight.w700,
                  letterSpacing: 1.2,
                ),
              ),
              if (showLanguageSwitch) const LanguageSwitchButton(),
            ],
          ),
          const SizedBox(height: 8),
          Text(
            title,
            style: GoogleFonts.cinzel(
              color: Colors.white,
              fontSize: 24,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            subtitle,
            style: GoogleFonts.plusJakartaSans(
              color: AppTheme.goldLight.withOpacity(0.9),
              fontSize: 13,
            ),
          ),
        ],
      ),
    );
  }
}

