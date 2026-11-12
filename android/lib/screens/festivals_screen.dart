import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import '../providers/language_provider.dart';
import '../utils/theme.dart';
import '../widgets/custom_card.dart';

class FestivalsScreen extends StatelessWidget {
  const FestivalsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final isTe = Provider.of<LanguageProvider>(context).isTelugu;

    final List<Map<String, dynamic>> festivals = [
      {
        "name_te": "సాలకట్ల వార్షిక బ్రహ్మోత్సవాలు",
        "name_en": "Salakatla Annual Brahmotsavam",
        "timing": "Ashwayuja Masa (September / October)",
        "desc_te": "బ్రహ్మదేవునిచే ఆరంభించబడిన 9 రోజుల మహా ఉత్సవం. ధ్వజారోహణం, గరుడ సేవ, రథోత్సవం మరియు చక్రస్నానం ప్రధాన ఘట్టాలు.",
        "desc_en": "Grand 9-day annual festival. Key events include Dhwajarohanam, Garuda Seva, Rathotsavam, and Chakrasnanam.",
        "icon": Icons.celebration,
        "color": const Color(0xFFD4AF37),
      },
      {
        "name_te": "వైకుంఠ ఏకాదశి (ముక్కోటి ఏకాదశి)",
        "name_en": "Vaikunta Ekadasi (Mukkoti Ekadasi)",
        "timing": "Dhanurmasa (December / January)",
        "desc_te": "పవిత్రమైన వైకుంఠ ద్వార దర్శనం 10 రోజుల పాటు భక్తులకు కల్పిస్తారు. ఈ ద్వార దర్శనం సకల పాపహరం మరియు మోక్షదాయకం.",
        "desc_en": "Sacred 10-day opening of holy Vaikunta Dwaram. Passing through the dwaram grants liberation and supreme blessings.",
        "icon": Icons.door_sliding,
        "color": const Color(0xFF800000),
      },
      {
        "name_te": "రథసప్తమి (ఒకరోజు బ్రహ్మోత్సవం)",
        "name_en": "Rathasapthami (Mini Brahmotsavam)",
        "timing": "Magha Shuddha Saptami (Jan / Feb)",
        "desc_te": "ఒకే రోజులో శ్రీ మలయప్ప స్వామివారు సూర్యోదయం నుండి రాత్రి వరకు 7 దివ్య వాహనాలపై తిరువీధుల్లో భక్తులకు దర్శనమిస్తారు.",
        "desc_en": "One-day Brahmotsavam where Lord Malayappa Swamy rides 7 divine vahanams in a single day around four mada streets.",
        "icon": Icons.wb_sunny,
        "color": const Color(0xFFFF9933),
      },
      {
        "name_te": "నెలవారీ పౌర్ణమి గరుడ సేవ",
        "name_en": "Monthly Pournami Garuda Seva",
        "timing": "Every Full Moon Night (పౌర్ణమి)",
        "desc_te": "ప్రతి పౌర్ణమి రాత్రి 7:00 నుండి 9:00 వరకు శ్రీ మలయప్ప స్వామివారు అత్యంత ప్రీతిపాత్రమైన గరుడ వాహనంపై తిరుమాడ వీధులలో విహరిస్తారు.",
        "desc_en": "Lord Malayappa Swamy rides majestically on Garuda Vahana every full moon night to bless gathered pilgrims.",
        "icon": Icons.brightness_2,
        "color": const Color(0xFF9C27B0),
      },
    ];

    return Scaffold(
      appBar: AppBar(
        title: Text(
          isTe ? "తిరుమల ఉత్సవాల క్యాలెండర్" : "Tirumala Festivals Calendar",
          style: GoogleFonts.cinzel(fontSize: 16, fontWeight: FontWeight.bold),
        ),
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: festivals.length,
        itemBuilder: (context, index) {
          final f = festivals[index];
          return Container(
            margin: const EdgeInsets.only(bottom: 14),
            child: CustomCard(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.all(10),
                        decoration: BoxDecoration(
                          color: (f['color'] as Color).withOpacity(0.12),
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: Icon(f['icon'] as IconData, color: f['color'] as Color, size: 24),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              isTe ? f['name_te'] : f['name_en'],
                              style: GoogleFonts.cinzel(
                                fontWeight: FontWeight.bold,
                                fontSize: 15,
                                color: AppTheme.maroonPrimary,
                              ),
                            ),
                            const SizedBox(height: 2),
                            Text(
                              f['timing'],
                              style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: AppTheme.goldDark),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  Text(
                    isTe ? f['desc_te'] : f['desc_en'],
                    style: const TextStyle(fontSize: 13, color: AppTheme.textMuted, height: 1.4),
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}

