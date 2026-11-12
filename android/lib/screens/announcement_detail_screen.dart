import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import 'package:share_plus/share_plus.dart';
import 'package:url_launcher/url_launcher.dart';
import '../models/announcement.dart';
import '../providers/language_provider.dart';
import '../providers/announcement_provider.dart';
import '../utils/theme.dart';
import '../utils/date_formatter.dart';
import '../widgets/status_badge.dart';

class AnnouncementDetailScreen extends StatelessWidget {
  final Announcement announcement;

  const AnnouncementDetailScreen({super.key, required this.announcement});

  @override
  Widget build(BuildContext context) {
    final lang = Provider.of<LanguageProvider>(context).currentLanguage;
    final isTe = lang == 'te';
    final annProvider = Provider.of<AnnouncementProvider>(context);

    return Scaffold(
      appBar: AppBar(
        title: Text(
          isTe ? "ప్రకటన వివరాలు" : "Announcement Details",
          style: GoogleFonts.cinzel(fontSize: 16, fontWeight: FontWeight.bold),
        ),
        actions: [
          IconButton(
            icon: Icon(
              announcement.isBookmarked ? Icons.bookmark : Icons.bookmark_border,
              color: announcement.isBookmarked ? AppTheme.goldLight : Colors.white,
            ),
            onPressed: () {
              annProvider.toggleBookmark(announcement);
            },
          ),
          IconButton(
            icon: const Icon(Icons.share),
            onPressed: () {
              Share.share(
                "${announcement.getTitle(lang)}\n\n${announcement.getContent(lang)}\n\nOfficial Source: ${announcement.sourceUrl}",
              );
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Status Badges
            Row(
              children: [
                if (announcement.isQuotaAlert) ...[
                  StatusBadge.quotaAlert(),
                  const SizedBox(width: 8),
                ],
                if (announcement.isVerified) StatusBadge.verified(),
              ],
            ),
            const SizedBox(height: 16),

            // Title
            Text(
              announcement.getTitle(lang),
              style: GoogleFonts.cinzel(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: AppTheme.maroonPrimary,
                height: 1.3,
              ),
            ),
            const SizedBox(height: 10),

            // Timestamp and Source Domain
            Row(
              children: [
                const Icon(Icons.calendar_today, size: 14, color: AppTheme.textMuted),
                const SizedBox(width: 6),
                Text(
                  DateFormatter.formatDevotionalDate(announcement.publicationDate, lang),
                  style: const TextStyle(fontSize: 12, color: AppTheme.textMuted),
                ),
                const Spacer(),
                Text(
                  announcement.sourceDomain,
                  style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: AppTheme.goldDark),
                ),
              ],
            ),

            const SizedBox(height: 16),
            const Divider(color: AppTheme.borderLight),
            const SizedBox(height: 16),

            // Full Content Text
            Text(
              announcement.getContent(lang),
              style: GoogleFonts.plusJakartaSans(
                fontSize: 15,
                color: AppTheme.textDark,
                height: 1.6,
              ),
            ),

            const SizedBox(height: 32),

            // Official Portal Verification Box
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: AppTheme.borderLight),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Icon(Icons.verified, color: Color(0xFF2E7D32), size: 20),
                      const SizedBox(width: 8),
                      Text(
                        isTe ? "అధికారిక మూలం & లింక్" : "Official Source & Verification",
                        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Text(
                    isTe
                        ? "ఈ సమాచారం టీటీడీ అధికారిక పోర్టల్ ద్వారా ప్రచురించబడింది. అసలు ప్రకటన చూడడానికి లేదా టికెట్లు బుక్ చేయడానికి క్రింది లింక్‌ను నొక్కండి."
                        : "This announcement is sourced directly from TTD official channels. Tap below to verify on the official website or proceed to booking.",
                    style: const TextStyle(fontSize: 12, color: AppTheme.textMuted, height: 1.4),
                  ),
                  const SizedBox(height: 14),
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton.icon(
                      icon: const Icon(Icons.open_in_new, size: 16),
                      label: Text(isTe ? "అధికారిక వెబ్‌సైట్ తెరవండి ↗" : "Open Official Portal ↗"),
                      onPressed: () async {
                        final uri = Uri.parse(announcement.sourceUrl);
                        if (await canLaunchUrl(uri)) {
                          await launchUrl(uri, mode: LaunchMode.externalApplication);
                        }
                      },
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 24),
            // Disclaimer
            Text(
              isTe
                  ? "నిరాకరణ: శ్రీవారి AI అనేది స్వతంత్ర సమాచార వేదిక. ఎలాంటి రుసుములు లేదా బుకింగ్ వివరాలను ఇక్కడ సేకరించబడవు."
                  : "Disclaimer: Srivari AI is an independent informational platform. No booking credentials or payments are handled on this app.",
              style: const TextStyle(fontSize: 11, color: AppTheme.textMuted),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}

