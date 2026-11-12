import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import 'package:url_launcher/url_launcher.dart';
import '../providers/language_provider.dart';
import '../utils/theme.dart';
import '../utils/constants.dart';

class AboutScreen extends StatelessWidget {
  const AboutScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final isTe = Provider.of<LanguageProvider>(context).isTelugu;

    return Scaffold(
      appBar: AppBar(
        title: Text(
          isTe ? "యాప్ గురించి" : "About Srivari AI",
          style: GoogleFonts.cinzel(fontSize: 16, fontWeight: FontWeight.bold),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            // Logo / Emblem
            Container(
              width: 90,
              height: 90,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: AppTheme.maroonPrimary,
                border: Border.all(color: AppTheme.goldPrimary, width: 2),
                boxShadow: [
                  BoxShadow(
                    color: AppTheme.goldPrimary.withOpacity(0.3),
                    blurRadius: 16,
                  )
                ],
              ),
              child: const Icon(Icons.temple_hindu, size: 48, color: AppTheme.goldLight),
            ),
            const SizedBox(height: 16),
            Text(
              "శ్రీవారి AI (Srivari AI)",
              style: GoogleFonts.cinzel(fontSize: 22, fontWeight: FontWeight.bold, color: AppTheme.maroonPrimary),
            ),
            const SizedBox(height: 4),
            Text(
              "Version 1.0.0 • Production Ready",
              style: const TextStyle(fontSize: 12, color: AppTheme.textMuted),
            ),

            const SizedBox(height: 24),

            // Mandatory Informational Disclaimer Card
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: const Color(0xFFFFFBEA),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: AppTheme.goldPrimary),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Icon(Icons.gavel, color: AppTheme.maroonPrimary, size: 20),
                      const SizedBox(width: 8),
                      Text(
                        isTe ? "ముఖ్యమైన చట్టపరమైన నిరాకరణ" : "Important Legal Disclaimer",
                        style: GoogleFonts.cinzel(fontWeight: FontWeight.bold, fontSize: 13, color: AppTheme.maroonPrimary),
                      ),
                    ],
                  ),
                  const SizedBox(height: 10),
                  Text(
                    isTe ? AppConstants.disclaimerTe : AppConstants.disclaimerEn,
                    style: const TextStyle(fontSize: 12, height: 1.5, color: AppTheme.textDark),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 24),

            // Official Portals List
            Align(
              alignment: Alignment.centerLeft,
              child: Text(
                isTe ? "అధికారిక టీటీడీ పోర్టల్స్" : "Official TTD Portals",
                style: GoogleFonts.cinzel(fontSize: 15, fontWeight: FontWeight.bold, color: AppTheme.maroonPrimary),
              ),
            ),
            const SizedBox(height: 10),

            _portalLink(
              title: "TTD Online Booking Portal",
              url: AppConstants.ttdBookingPortal,
              desc: "Darshan, Seva, Accommodation, and Hundi bookings",
            ),
            _portalLink(
              title: "TTD Official News Portal",
              url: AppConstants.ttdNewsPortal,
              desc: "Official press releases, quota announcements, and tenders",
            ),
            _portalLink(
              title: "Tirumala Main Portal",
              url: AppConstants.ttdMainPortal,
              desc: "Temple history, administration, and ritual details",
            ),

            const SizedBox(height: 28),

            Text(
              "సర్వే జనాః సుఖినో భవన్తు • లోకాః సమస్తాః సుఖినో భవన్తు",
              style: GoogleFonts.cinzel(fontSize: 12, color: AppTheme.textMuted, fontStyle: FontStyle.italic),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 16),
          ],
        ),
      ),
    );
  }

  Widget _portalLink({
    required String title,
    required String url,
    required String desc,
  }) {
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: AppTheme.borderLight),
      ),
      child: ListTile(
        title: Text(title, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold)),
        subtitle: Text(desc, style: const TextStyle(fontSize: 11, color: AppTheme.textMuted)),
        trailing: const Icon(Icons.open_in_new, size: 18, color: AppTheme.maroonPrimary),
        onTap: () async {
          final uri = Uri.parse(url);
          if (await canLaunchUrl(uri)) {
            await launchUrl(uri, mode: LaunchMode.externalApplication);
          }
        },
      ),
    );
  }
}

