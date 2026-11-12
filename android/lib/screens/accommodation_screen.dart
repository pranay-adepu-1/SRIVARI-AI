import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import 'package:url_launcher/url_launcher.dart';
import '../providers/language_provider.dart';
import '../utils/theme.dart';
import '../utils/constants.dart';
import '../widgets/custom_card.dart';

class AccommodationScreen extends StatelessWidget {
  const AccommodationScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final isTe = Provider.of<LanguageProvider>(context).isTelugu;

    return Scaffold(
      appBar: AppBar(
        title: Text(
          isTe ? "తిరుమల వసతి & గదుల వివరాలు" : "Accommodation & Cottages",
          style: GoogleFonts.cinzel(fontSize: 16, fontWeight: FontWeight.bold),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 24-Hour Rule Warning Box
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: const Color(0xFFFFF3E0),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: Colors.orange.shade300),
              ),
              child: Row(
                children: [
                  const Icon(Icons.warning_amber_rounded, color: Colors.deepOrange, size: 26),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      isTe
                          ? "గరిష్ట బస పరిమితి: తిరుమలలో గదులు గరిష్టంగా 24 గంటలు మాత్రమే కేటాయిస్తారు. ఎలాంటి పొడిగింపు ఉండదు."
                          : "24-Hour Rule: Accommodation in Tirumala is strictly allotted for 24 hours only. No extensions granted.",
                      style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.black87),
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 20),

            // Tirumala Cottages Card
            CustomCard(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        isTe ? "తిరుమల కాటేజీలు & విశ్రాంతి భవనాలు" : "Tirumala Cottages & Rest Houses",
                        style: GoogleFonts.cinzel(
                          fontWeight: FontWeight.bold,
                          fontSize: 15,
                          color: AppTheme.maroonPrimary,
                        ),
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        decoration: BoxDecoration(
                          color: AppTheme.goldPrimary.withOpacity(0.15),
                          borderRadius: BorderRadius.circular(6),
                        ),
                        child: const Text("₹100 - ₹2,000", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 11)),
                      ),
                    ],
                  ),
                  const SizedBox(height: 10),
                  Text(
                    isTe
                        ? "• ఆన్‌లైన్ కోటా: ttdevasthanams.ap.gov.in లో 3 నెలల ముందే విడుదల.\n• కరెంట్ బుకింగ్: తిరుమల సిఆర్ఓ (CRO) జనరల్ కౌంటర్ వద్ద లభిస్తుంది.\n• రిపోర్టింగ్ సమయం: కేటాయించిన స్లాట్ సమయం నుండి 3 గంటల లోపు సబ్-ఎంక్వైరీ ఆఫీస్‌లో రిపోర్ట్ చేయాలి.\n• కాషన్ డిపాజిట్: గది అద్దెతో సమానమైన డిపాజిట్ చెల్లించాలి. గది ఖాళీ చేసిన 3-7 రోజుల్లో బ్యాంక్ ఖాతాకు తిరిగి వస్తుంది."
                        : "• Online Quota: Released monthly, 3 months in advance on ttdevasthanams.ap.gov.in.\n• Current Booking: Available at Central Reception Office (CRO) General counter.\n• Reporting Window: Must report within 3 hours from the allotted slot time.\n• Caution Deposit: Equal to room tariff. Automatically refunded to bank account within 3–7 business days upon checkout.",
                    style: const TextStyle(fontSize: 13, height: 1.5, color: AppTheme.textDark),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 16),

            // Tirupati Rest Houses Card
            CustomCard(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        isTe ? "తిరుపతి విశ్రాంతి భవనాలు" : "Tirupati Downhill Rest Houses",
                        style: GoogleFonts.cinzel(
                          fontWeight: FontWeight.bold,
                          fontSize: 15,
                          color: AppTheme.maroonPrimary,
                        ),
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        decoration: BoxDecoration(
                          color: Colors.green.withOpacity(0.15),
                          borderRadius: BorderRadius.circular(6),
                        ),
                        child: const Text("₹200 - ₹1,500", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 11, color: Colors.green)),
                      ),
                    ],
                  ),
                  const SizedBox(height: 10),
                  Text(
                    isTe
                        ? "• శ్రీనివాసం కాంప్లెక్స్: తిరుపతి ఆర్టీసీ సెంట్రల్ బస్ స్టాండ్ ఎదురుగా.\n• విష్ణు నివాసం: తిరుపతి రైల్వే స్టేషన్ ఎదురుగా.\n• మాధవం కాంప్లెక్స్: శ్రీనివాసం కాంప్లెక్స్ సమీపంలో.\n• కౌంటర్లలో స్పాట్ బుకింగ్ మరియు ఆన్‌లైన్ అడ్వాన్స్ బుకింగ్ రెండూ అందుబాటులో ఉంటాయి."
                        : "• Srinivasam Complex: Opposite RTC Central Bus Stand, Tirupati.\n• Vishnu Nivasam: Opposite Tirupati Main Railway Station.\n• Madhavan Rest House: Adjacent to Srinivasam Complex.\n• Both current spot booking and online advance quotas available.",
                    style: const TextStyle(fontSize: 13, height: 1.5, color: AppTheme.textDark),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 24),

            // Booking Button CTA
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton.icon(
                icon: const Icon(Icons.hotel_outlined),
                label: Text(
                  isTe ? "అధికారిక వెబ్‌సైట్‌లో గదులు బుక్ చేయండి ↗" : "Book Rooms on Official Portal ↗",
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

