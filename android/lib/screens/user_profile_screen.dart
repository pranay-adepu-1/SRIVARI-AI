import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import '../providers/language_provider.dart';
import '../providers/announcement_provider.dart';
import '../utils/theme.dart';
import 'saved_announcements_screen.dart';
import 'settings_screen.dart';
import 'about_screen.dart';

class UserProfileScreen extends StatelessWidget {
  const UserProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final isTe = Provider.of<LanguageProvider>(context).isTelugu;
    final annProvider = Provider.of<AnnouncementProvider>(context);

    return Scaffold(
      appBar: AppBar(
        title: Text(
          isTe ? "భక్తుని ప్రొఫైల్" : "Devotee Profile",
          style: GoogleFonts.cinzel(fontSize: 16, fontWeight: FontWeight.bold),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            // Avatar
            Center(
              child: Column(
                children: [
                  Container(
                    width: 84,
                    height: 84,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: AppTheme.maroonPrimary.withOpacity(0.1),
                      border: Border.all(color: AppTheme.goldPrimary, width: 2),
                    ),
                    child: const Icon(Icons.person, size: 46, color: AppTheme.maroonPrimary),
                  ),
                  const SizedBox(height: 12),
                  Text(
                    isTe ? "శ్రీవారి భక్తుడు" : "Srivari Devotee",
                    style: GoogleFonts.cinzel(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    "॥ ఓం నమో వేంకటేశాయ ॥",
                    style: TextStyle(fontSize: 12, color: AppTheme.goldDark, fontWeight: FontWeight.bold),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 28),

            // Options List
            _profileOption(
              icon: Icons.bookmark,
              title: isTe ? "సేవ్ చేసిన ప్రకటనలు" : "Saved Announcements",
              trailing: "${annProvider.bookmarks.length}",
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => const SavedAnnouncementsScreen()),
                );
              },
            ),
            _profileOption(
              icon: Icons.settings,
              title: isTe ? "యాప్ సెట్టింగ్స్" : "App Settings",
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => const SettingsScreen()),
                );
              },
            ),
            _profileOption(
              icon: Icons.info_outline,
              title: isTe ? "యాప్ గురించి & అధికారిక లింకులు" : "About & Official TTD Links",
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => const AboutScreen()),
                );
              },
            ),

            const SizedBox(height: 28),

            // Devotional Quote Box
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: const Color(0xFFFFF9E6),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: AppTheme.goldPrimary.withOpacity(0.5)),
              ),
              child: Column(
                children: [
                  Text(
                    "శ్రీ వేంకటేశ్వర స్తోత్రం",
                    style: GoogleFonts.cinzel(fontWeight: FontWeight.bold, fontSize: 13, color: AppTheme.maroonPrimary),
                  ),
                  const SizedBox(height: 6),
                  const Text(
                    "కమలాకుచ చూచుక కుంకుమతో\nనియతారుణితాతుల నీలతనో!\nకమలాయతలోచన! లోకపతే!\nవిజయీభవ! వేంకటశైలపతే!",
                    style: TextStyle(fontSize: 12, height: 1.5, color: AppTheme.textDark),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _profileOption({
    required IconData icon,
    required String title,
    String? trailing,
    required VoidCallback onTap,
  }) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppTheme.borderLight),
      ),
      child: ListTile(
        leading: Icon(icon, color: AppTheme.maroonPrimary),
        title: Text(title, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600)),
        trailing: trailing != null
            ? Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                decoration: BoxDecoration(
                  color: AppTheme.maroonPrimary.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(trailing, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
              )
            : const Icon(Icons.chevron_right, color: AppTheme.borderLight),
        onTap: onTap,
      ),
    );
  }
}

