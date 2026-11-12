import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import 'package:url_launcher/url_launcher.dart';
import '../providers/language_provider.dart';
import '../services/api_service.dart';
import '../models/darshan_info.dart';
import '../utils/theme.dart';
import '../utils/constants.dart';
import '../widgets/custom_card.dart';

class DarshanScreen extends StatefulWidget {
  const DarshanScreen({super.key});

  @override
  State<DarshanScreen> createState() => _DarshanScreenState();
}

class _DarshanScreenState extends State<DarshanScreen> {
  final ApiService _apiService = ApiService();
  List<DarshanGuideItem> _guides = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadGuides();
  }

  Future<void> _loadGuides() async {
    final list = await _apiService.getDarshanGuides();
    setState(() {
      _guides = list;
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    final isTe = Provider.of<LanguageProvider>(context).isTelugu;
    final lang = isTe ? 'te' : 'en';

    return Scaffold(
      appBar: AppBar(
        title: Text(
          isTe ? "శ్రీవారి దర్శన మార్గదర్శకాలు" : "Srivari Darshan Guides",
          style: GoogleFonts.cinzel(fontSize: 16, fontWeight: FontWeight.bold),
        ),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator(color: AppTheme.maroonPrimary))
          : SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Dress Code Alert Box
                  Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: const Color(0xFFFFF9E6),
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: AppTheme.goldPrimary),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            const Icon(Icons.checkroom, color: AppTheme.maroonPrimary, size: 22),
                            const SizedBox(width: 8),
                            Text(
                              isTe ? "సాంప్రదాయ వస్త్రధారణ తప్పనిసరి" : "Mandatory Traditional Dress Code",
                              style: GoogleFonts.cinzel(
                                fontWeight: FontWeight.bold,
                                fontSize: 14,
                                color: AppTheme.maroonPrimary,
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Text(
                          isTe
                              ? "• పురుషులకు: తెల్లటి పంచె (ధోతీ) మరియు కుర్తా లేదా పైజామా.\n• మహిళలకు: చీర, లంగా ఓణీ లేదా దుపట్టాతో కూడిన చుడీదార్.\n• టీ-షర్టులు, జీన్స్, లఘాలు, వెస్ట్రన్ దుస్తులు అనుమతించబడవు."
                              : "• Men: Dhoti/Kurta, Pyjama with Kurta or Uttariyam.\n• Women: Saree, Half Saree, or Chudidar with Dupatta.\n• Strictly prohibited: T-shirts, Jeans, Shorts, and western attire.",
                          style: const TextStyle(fontSize: 12, height: 1.5, color: AppTheme.textDark),
                        ),
                      ],
                    ),
                  ),

                  const SizedBox(height: 20),

                  Text(
                    isTe ? "దర్శన రకాలు & వివరాలు" : "Darshan Types & Guidelines",
                    style: GoogleFonts.cinzel(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: AppTheme.maroonPrimary,
                    ),
                  ),

                  const SizedBox(height: 12),

                  ..._guides.map((g) => _buildDarshanCard(g, lang, isTe)),

                  const SizedBox(height: 16),

                  // Booking Link CTA
                  SizedBox(
                    width: double.infinity,
                    height: 50,
                    child: ElevatedButton.icon(
                      icon: const Icon(Icons.open_in_new),
                      label: Text(
                        isTe ? "అధికారిక టీటీడీ పోర్టల్‌లో బుక్ చేయండి ↗" : "Book on Official TTD Portal ↗",
                      ),
                      onPressed: () async {
                        final uri = Uri.parse(AppConstants.ttdBookingPortal);
                        if (await canLaunchUrl(uri)) {
                          await launchUrl(uri, mode: LaunchMode.externalApplication);
                        }
                      },
                    ),
                  ),
                  const SizedBox(height: 24),
                ],
              ),
            ),
    );
  }

  Widget _buildDarshanCard(DarshanGuideItem guide, String lang, bool isTe) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      child: CustomCard(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Expanded(
                  child: Text(
                    guide.getName(lang),
                    style: GoogleFonts.cinzel(
                      fontWeight: FontWeight.bold,
                      fontSize: 15,
                      color: AppTheme.maroonPrimary,
                    ),
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: AppTheme.goldPrimary.withOpacity(0.15),
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: Text(
                    guide.cost,
                    style: const TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 12,
                      color: AppTheme.goldDark,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Text(
              guide.getDescription(lang),
              style: const TextStyle(fontSize: 13, color: AppTheme.textMuted, height: 1.4),
            ),
            const SizedBox(height: 10),
            Row(
              children: [
                const Icon(Icons.location_on_outlined, size: 14, color: AppTheme.maroonPrimary),
                const SizedBox(width: 4),
                Expanded(
                  child: Text(
                    "${isTe ? 'రిపోర్టింగ్:' : 'Reporting:'} ${guide.getReportingLocation(lang)}",
                    style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            const Text(
              "Important Guidelines:",
              style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: AppTheme.textDark),
            ),
            const SizedBox(height: 6),
            ...guide.getGuidelines(lang).map(
              (rule) => Padding(
                padding: const EdgeInsets.symmetric(vertical: 2.0),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text("• ", style: TextStyle(color: AppTheme.goldDark, fontWeight: FontWeight.bold)),
                    Expanded(
                      child: Text(
                        rule,
                        style: const TextStyle(fontSize: 12, color: AppTheme.textMuted, height: 1.4),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

