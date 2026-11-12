import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import '../providers/language_provider.dart';
import '../providers/theme_provider.dart';
import '../utils/theme.dart';
import 'about_screen.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  bool _dailyDigestEnabled = true;
  bool _quotaAlertsEnabled = true;

  @override
  Widget build(BuildContext context) {
    final langProvider = Provider.of<LanguageProvider>(context);
    final themeProvider = Provider.of<ThemeProvider>(context);
    final isTe = langProvider.isTelugu;

    return Scaffold(
      appBar: AppBar(
        title: Text(
          isTe ? "యాప్ సెట్టింగ్స్" : "Settings",
          style: GoogleFonts.cinzel(fontSize: 16, fontWeight: FontWeight.bold),
        ),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Section: Language
          _sectionTitle(isTe ? "భాష ఎంపిక (Language)" : "Language Selection"),
          Container(
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: AppTheme.borderLight),
            ),
            child: Column(
              children: [
                RadioListTile<String>(
                  title: const Text("తెలుగు (Telugu)", style: TextStyle(fontWeight: FontWeight.bold)),
                  value: 'te',
                  groupValue: langProvider.currentLanguage,
                  activeColor: AppTheme.maroonPrimary,
                  onChanged: (val) => langProvider.setLanguage('te'),
                ),
                const Divider(height: 1),
                RadioListTile<String>(
                  title: const Text("English", style: TextStyle(fontWeight: FontWeight.bold)),
                  value: 'en',
                  groupValue: langProvider.currentLanguage,
                  activeColor: AppTheme.maroonPrimary,
                  onChanged: (val) => langProvider.setLanguage('en'),
                ),
              ],
            ),
          ),

          const SizedBox(height: 24),

          // Section: Notifications
          _sectionTitle(isTe ? "నోటిఫికేషన్లు (Notifications)" : "Notifications"),
          Container(
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: AppTheme.borderLight),
            ),
            child: Column(
              children: [
                SwitchListTile(
                  title: Text(
                    isTe ? "రోజువారీ తిరుమల సమాచారం (8:00 AM)" : "Daily Tirumala Digest (8:00 AM IST)",
                    style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
                  ),
                  subtitle: Text(
                    isTe ? "నిరీక్షణ సమయాలు, సర్వ దర్శనం టోకెన్ స్థితి" : "Waiting times, SSD token status, daily quote",
                    style: const TextStyle(fontSize: 12),
                  ),
                  value: _dailyDigestEnabled,
                  activeColor: AppTheme.maroonPrimary,
                  onChanged: (val) => setState(() => _dailyDigestEnabled = val),
                ),
                const Divider(height: 1),
                SwitchListTile(
                  title: Text(
                    isTe ? "కోటా విడుదల హెచ్చరికలు" : "Instant Quota Release Alerts",
                    style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
                  ),
                  subtitle: Text(
                    isTe ? "రూ. 300 SED, సేవలు, గదుల కోటా విడుదల" : "₹300 SED, Seva, and accommodation online openings",
                    style: const TextStyle(fontSize: 12),
                  ),
                  value: _quotaAlertsEnabled,
                  activeColor: AppTheme.maroonPrimary,
                  onChanged: (val) => setState(() => _quotaAlertsEnabled = val),
                ),
              ],
            ),
          ),

          const SizedBox(height: 24),

          // Section: Appearance
          _sectionTitle(isTe ? "థీమ్ (Theme)" : "Appearance"),
          Container(
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: AppTheme.borderLight),
            ),
            child: SwitchListTile(
              title: Text(
                isTe ? "డార్క్ మోడ్ (Dark Mode)" : "Dark Mode",
                style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
              ),
              value: themeProvider.isDarkMode,
              activeColor: AppTheme.maroonPrimary,
              onChanged: (_) => themeProvider.toggleTheme(),
            ),
          ),

          const SizedBox(height: 24),

          // Section: General
          _sectionTitle(isTe ? "సమాచారం & సహాయం" : "About & Support"),
          Container(
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: AppTheme.borderLight),
            ),
            child: Column(
              children: [
                ListTile(
                  leading: const Icon(Icons.info_outline, color: AppTheme.maroonPrimary),
                  title: Text(
                    isTe ? "యాప్ గురించి & అధికారిక లింకులు" : "About App & Official Links",
                    style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
                  ),
                  trailing: const Icon(Icons.chevron_right),
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (_) => const AboutScreen()),
                    );
                  },
                ),
                const Divider(height: 1),
                ListTile(
                  leading: const Icon(Icons.cleaning_services_outlined, color: AppTheme.maroonPrimary),
                  title: Text(
                    isTe ? "కాష్ తొలగించండి (Clear Cache)" : "Clear Local Cache",
                    style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
                  ),
                  onTap: () {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text(isTe ? "కాష్ విజయవంతంగా తొలగించబడింది" : "Cache cleared successfully")),
                    );
                  },
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),
        ],
      ),
    );
  }

  Widget _sectionTitle(String title) {
    return Padding(
      padding: const EdgeInsets.only(left: 4, bottom: 8),
      child: Text(
        title,
        style: GoogleFonts.cinzel(
          fontSize: 13,
          fontWeight: FontWeight.bold,
          color: AppTheme.maroonPrimary,
        ),
      ),
    );
  }
}

