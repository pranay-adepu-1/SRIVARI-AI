import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import '../providers/announcement_provider.dart';
import '../providers/language_provider.dart';
import '../utils/theme.dart';
import '../widgets/announcement_card.dart';
import 'announcement_detail_screen.dart';

class SavedAnnouncementsScreen extends StatelessWidget {
  const SavedAnnouncementsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final annProvider = Provider.of<AnnouncementProvider>(context);
    final isTe = Provider.of<LanguageProvider>(context).isTelugu;

    return Scaffold(
      appBar: AppBar(
        title: Text(
          isTe ? "సేవ్ చేసిన ప్రకటనలు" : "Saved Announcements",
          style: GoogleFonts.cinzel(fontSize: 16, fontWeight: FontWeight.bold),
        ),
      ),
      body: annProvider.bookmarks.isEmpty
          ? Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.bookmark_border, size: 54, color: AppTheme.textMuted),
                  const SizedBox(height: 12),
                  Text(
                    isTe ? "సేవ్ చేసిన ప్రకటనలు ఏవీ లేవు" : "No saved announcements yet",
                    style: const TextStyle(color: AppTheme.textMuted, fontSize: 14),
                  ),
                ],
              ),
            )
          : ListView.builder(
              padding: const EdgeInsets.symmetric(vertical: 12),
              itemCount: annProvider.bookmarks.length,
              itemBuilder: (context, index) {
                final item = annProvider.bookmarks[index];
                return AnnouncementCard(
                  announcement: item,
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => AnnouncementDetailScreen(announcement: item),
                      ),
                    );
                  },
                );
              },
            ),
    );
  }
}

