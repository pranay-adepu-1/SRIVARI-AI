import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import 'package:url_launcher/url_launcher.dart';
import '../providers/language_provider.dart';
import '../utils/theme.dart';
import '../utils/constants.dart';
import '../widgets/custom_card.dart';

class SrivariSevaScreen extends StatelessWidget {
  const SrivariSevaScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final isTe = Provider.of<LanguageProvider>(context).isTelugu;

    return Scaffold(
      appBar: AppBar(
        title: Text(
          isTe ? "శ్రీవారి సేవ మార్గదర్శకాలు" : "Srivari Seva Guidelines",
          style: GoogleFonts.cinzel(fontSize: 16, fontWeight: FontWeight.bold),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Divine Banner
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  colors: [AppTheme.maroonDeep, AppTheme.maroonPrimary],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                borderRadius: BorderRadius.circular(14),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Icon(Icons.volunteer_activism, color: AppTheme.goldLight, size: 28),
                      const SizedBox(width: 10),
                      Text(
                        isTe ? "మానవ సేవే మాధవ సేవ" : "Service to Devotees is Service to God",
                        style: GoogleFonts.cinzel(
                          color: AppTheme.goldLight,
                          fontWeight: FontWeight.bold,
                          fontSize: 15,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 10),
                  Text(
                    isTe
                        ? "శ్రీ వేంకటేశ్వర స్వామివారి దివ్య క్షేత్రంలో భక్తులకు నిస్వార్థ భక్తిభావంతో సేవలు అందించే పవిత్ర స్వచ్ఛంద అవకాశం."
                        : "A sacred opportunity to render voluntary devotional service to millions of pilgrims visiting Tirumala hills.",
                    style: const TextStyle(color: Colors.white, fontSize: 13, height: 1.4),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 20),

            // Eligibility Card
            CustomCard(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Icon(Icons.assignment_ind_outlined, color: AppTheme.maroonPrimary, size: 20),
                      const SizedBox(width: 8),
                      Text(
                        isTe ? "అర్హతలు & వయోపరిమితి" : "Eligibility Criteria",
                        style: GoogleFonts.cinzel(fontWeight: FontWeight.bold, fontSize: 15),
                      ),
                    ],
                  ),
                  const SizedBox(height: 10),
                  Text(
                    isTe
                        ? "• వయస్సు: 18 నుండి 60 సంవత్సరాల మధ్య ఉండాలి.\n• శారీరక, మానసిక దృఢత్వం తప్పనిసరి.\n• హిందూ మతస్థులై ఉండాలి.\n• పరకామణి సేవకు: 35 నుండి 65 ఏళ్ల బ్యాంకింగ్ లేదా ప్రభుత్వ ఉద్యోగులు/రిటైర్డ్ అధికారులు మాత్రమే అర్హులు."
                        : "• Age: Between 18 and 60 years old.\n• Physical & mental fitness is compulsory.\n• Must profess Hindu faith.\n• Parakamani Seva: Open only to retired/working bank/govt officers aged 35 to 65.",
                    style: const TextStyle(fontSize: 13, height: 1.5, color: AppTheme.textDark),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 14),

            // Dress Code Card
            CustomCard(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Icon(Icons.checkroom, color: AppTheme.goldDark, size: 20),
                      const SizedBox(width: 8),
                      Text(
                        isTe ? "సేవకుల వస్త్రధారణ" : "Sevaks Dress Code",
                        style: GoogleFonts.cinzel(fontWeight: FontWeight.bold, fontSize: 15),
                      ),
                    ],
                  ),
                  const SizedBox(height: 10),
                  Text(
                    isTe
                        ? "• మహిళా సేవకులు: చీర మరియు మెడలో కుంకుమ రంగు కండువా (కవచం).\n• పురుష సేవకులు: తెల్లటి పంచె/కుర్తా లేదా తెల్లటి చొక్కా/ప్యాంట్ మరియు పసుపు రంగు కండువా.\n• సేవకులు తప్పనిసరిగా తిలక ధారణ (గోపీచందనం లేదా విభూతి) చేయాలి."
                        : "• Female Sevaks: Traditional Saree with sacred Maroon scarf (Kavacham).\n• Male Sevaks: White Dhoti/Kurta or White Shirt/Pant with sacred Yellow scarf.\n• Devotional Tilak/Namam is mandatory during duty.",
                    style: const TextStyle(fontSize: 13, height: 1.5, color: AppTheme.textDark),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 14),

            // Tenure & Reporting
            CustomCard(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Icon(Icons.schedule, color: Color(0xFF2E7D32), size: 20),
                      const SizedBox(width: 8),
                      Text(
                        isTe ? "సేవా కాలం & రిపోర్టింగ్" : "Tenure & Reporting",
                        style: GoogleFonts.cinzel(fontWeight: FontWeight.bold, fontSize: 15),
                      ),
                    ],
                  ),
                  const SizedBox(height: 10),
                  Text(
                    isTe
                        ? "• సేవా కాలం: సాధారణంగా 7 రోజుల వ్యవధి (ప్రతి శుక్రవారం లేదా మంగళవారం రిపోర్ట్ చేయాలి).\n• రిపోర్టింగ్ కేంద్రం: శ్రీవారి సేవా సదన్, పీఏసీ-4, తిరుమల.\n• వసతి & భోజనం: సేవా కాలంలో టీటీడీ ఉచిత వసతి మరియు అన్నప్రసాదం కల్పిస్తుంది."
                        : "• Duration: Standard 7-day tenure (Reporting on Fridays/Tuesdays) or 4-day special slots.\n• Reporting Location: Srivari Seva Sadan, PAC-4, Tirumala.\n• Free Accommodation & Annaprasadam provided by TTD during tenure.",
                    style: const TextStyle(fontSize: 13, height: 1.5, color: AppTheme.textDark),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 24),

            // Registration Action Button
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton.icon(
                icon: const Icon(Icons.how_to_reg),
                label: Text(
                  isTe ? "ఉచితంగా సేవకు నమోదు చేసుకోండి ↗" : "Register for Srivari Seva Online ↗",
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
}

