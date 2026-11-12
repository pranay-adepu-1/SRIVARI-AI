import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import '../providers/language_provider.dart';
import '../providers/announcement_provider.dart';
import '../utils/theme.dart';
import '../widgets/tirumala_header.dart';
import '../widgets/quick_action_button.dart';
import '../widgets/announcement_card.dart';
import '../widgets/disclaimer_banner.dart';
import 'chat_screen.dart';
import 'announcements_screen.dart';
import 'announcement_detail_screen.dart';
import 'darshan_screen.dart';
import 'srivari_seva_screen.dart';
import 'accommodation_screen.dart';
import 'festivals_screen.dart';
import 'voice_assistant_screen.dart';
import 'notification_center_screen.dart';
import 'settings_screen.dart';

class HomeDashboardScreen extends StatefulWidget {
  const HomeDashboardScreen({super.key});

  @override
  State<HomeDashboardScreen> createState() => _HomeDashboardScreenState();
}

class _HomeDashboardScreenState extends State<HomeDashboardScreen> {
  int _currentNavIndex = 0;

  @override
  Widget build(BuildContext context) {
    final langProvider = Provider.of<LanguageProvider>(context);
    final isTe = langProvider.isTelugu;
    final annProvider = Provider.of<AnnouncementProvider>(context);

    final List<Widget> navScreens = [
      _buildHomeContent(context, isTe, annProvider),
      const AnnouncementsScreen(),
      const ChatScreen(),
      const VoiceAssistantScreen(),
      const SettingsScreen(),
    ];

    return Scaffold(
      body: navScreens[_currentNavIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _currentNavIndex,
        onDestinationSelected: (index) {
          setState(() => _currentNavIndex = index);
        },
        backgroundColor: Colors.white,
        elevation: 4,
        indicatorColor: AppTheme.maroonPrimary.withOpacity(0.12),
        destinations: [
          NavigationDestination(
            icon: const Icon(Icons.home_outlined),
            selectedIcon: const Icon(Icons.home, color: AppTheme.maroonPrimary),
            label: isTe ? "హోమ్" : "Home",
          ),
          NavigationDestination(
            icon: const Icon(Icons.campaign_outlined),
            selectedIcon: const Icon(Icons.campaign, color: AppTheme.maroonPrimary),
            label: isTe ? "ప్రకటనలు" : "News",
          ),
          NavigationDestination(
            icon: const Icon(Icons.psychology_outlined),
            selectedIcon: const Icon(Icons.psychology, color: AppTheme.maroonPrimary),
            label: isTe ? "AI చాట్" : "AI Chat",
          ),
          NavigationDestination(
            icon: const Icon(Icons.mic_none),
            selectedIcon: const Icon(Icons.mic, color: AppTheme.maroonPrimary),
            label: isTe ? "వాయిస్" : "Voice",
          ),
          NavigationDestination(
            icon: const Icon(Icons.settings_outlined),
            selectedIcon: const Icon(Icons.settings, color: AppTheme.maroonPrimary),
            label: isTe ? "సెట్టింగ్స్" : "Settings",
          ),
        ],
      ),
    );
  }

  Widget _buildHomeContent(BuildContext context, bool isTe, AnnouncementProvider annProvider) {
    return RefreshIndicator(
      onRefresh: () async {
        await annProvider.loadAnnouncements();
      },
      color: AppTheme.maroonPrimary,
      child: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Divine Tirumala Header
            TirumalaHeader(
              title: isTe ? "శ్రీవారి AI" : "Srivari AI",
              subtitle: isTe
                  ? "మీ ఆధికారిక ఆధ్యాత్మిక తిరుమల సమాచార వేదిక"
                  : "Your Intelligent Tirumala Devotee Assistant",
            ),

            // Top Notice & Notification Bell Row
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 10),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.all(6),
                        decoration: BoxDecoration(
                          color: AppTheme.saffronAccent.withOpacity(0.15),
                          borderRadius: BorderRadius.circular(6),
                        ),
                        child: const Icon(Icons.wb_sunny, size: 16, color: AppTheme.saffronAccent),
                      ),
                      const SizedBox(width: 8),
                      Text(
                        isTe ? "గోవిందా గోవిందా! స్వామివారి ఆశీస్సులు" : "Govinda Govinda! Srivari Blessings",
                        style: GoogleFonts.cinzel(
                          fontWeight: FontWeight.bold,
                          fontSize: 13,
                          color: AppTheme.maroonPrimary,
                        ),
                      ),
                    ],
                  ),
                  IconButton(
                    icon: const Icon(Icons.notifications_outlined, color: AppTheme.maroonPrimary),
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (_) => const NotificationCenterScreen()),
                      );
                    },
                  ),
                ],
              ),
            ),

            // AI Search Bar Pill
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16.0),
              child: Material(
                color: Colors.white,
                elevation: 2,
                borderRadius: BorderRadius.circular(30),
                child: InkWell(
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (_) => const ChatScreen()),
                    );
                  },
                  borderRadius: BorderRadius.circular(30),
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                    decoration: BoxDecoration(
                      border: Border.all(color: AppTheme.borderLight),
                      borderRadius: BorderRadius.circular(30),
                    ),
                    child: Row(
                      children: [
                        const Icon(Icons.search, color: AppTheme.maroonPrimary),
                        const SizedBox(width: 10),
                        Expanded(
                          child: Text(
                            isTe
                                ? "దర్శనం, సేవలు, గదులు లేదా లడ్డూ వివరాలు అడగండి..."
                                : "Ask about ₹300 Darshan, Seva, cottages, waiting times...",
                            style: GoogleFonts.plusJakartaSans(
                              fontSize: 13,
                              color: AppTheme.textMuted,
                            ),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                          decoration: BoxDecoration(
                            color: AppTheme.goldPrimary,
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: const Text(
                            "AI",
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 11,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),

            const SizedBox(height: 16),

            // Live Darshan & Waiting Time Card
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16.0),
              child: Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [Color(0xFF381204), Color(0xFF5B1A04)],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  borderRadius: BorderRadius.circular(14),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.12),
                      blurRadius: 8,
                      offset: const Offset(0, 3),
                    )
                  ],
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Row(
                          children: [
                            const Icon(Icons.access_time_filled, color: AppTheme.goldLight, size: 16),
                            const SizedBox(width: 6),
                            Text(
                              isTe ? "నేటి తిరుమల స్థితి (Live Update)" : "Tirumala Live Status Update",
                              style: GoogleFonts.cinzel(
                                color: AppTheme.goldLight,
                                fontWeight: FontWeight.bold,
                                fontSize: 13,
                              ),
                            ),
                          ],
                        ),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                          decoration: BoxDecoration(
                            color: Colors.green.withOpacity(0.2),
                            borderRadius: BorderRadius.circular(4),
                          ),
                          child: const Text(
                            "TODAY",
                            style: TextStyle(color: Colors.greenAccent, fontSize: 10, fontWeight: FontWeight.bold),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        _statusMetric(
                          isTe ? "సర్వ దర్శనం" : "Sarva Darshan",
                          isTe ? "12-14 గంటలు" : "12-14 hrs",
                          Icons.people_outline,
                        ),
                        Container(width: 1, height: 36, color: Colors.white24),
                        _statusMetric(
                          isTe ? "కంపార్ట్‌మెంట్లు" : "Compartments",
                          isTe ? "18 నిండినవి" : "18 Full",
                          Icons.grid_view,
                        ),
                        Container(width: 1, height: 36, color: Colors.white24),
                        _statusMetric(
                          isTe ? "రూ. 300 SED" : "₹300 SED",
                          isTe ? "2-3 గంటలు" : "2-3 hrs",
                          Icons.speed,
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 20),

            // Quick Services Section
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16.0),
              child: Text(
                isTe ? "ముఖ్యమైన దేవస్థాన సేవలు" : "Temple Services & Guides",
                style: GoogleFonts.cinzel(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: AppTheme.maroonPrimary,
                ),
              ),
            ),
            const SizedBox(height: 12),

            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16.0),
              child: Column(
                children: [
                  Row(
                    children: [
                      Expanded(
                        child: QuickActionButton(
                          title: isTe ? "దర్శనం" : "Darshan",
                          subtitle: isTe ? "రూ. 300, సర్వ, VIP" : "SED, Sarva, VIP",
                          icon: Icons.visibility,
                          onTap: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(builder: (_) => const DarshanScreen()),
                            );
                          },
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: QuickActionButton(
                          title: isTe ? "శ్రీవారి సేవ" : "Srivari Seva",
                          subtitle: isTe ? "స్వచ్ఛంద సేవ" : "Voluntary Service",
                          icon: Icons.volunteer_activism,
                          iconColor: AppTheme.saffronAccent,
                          onTap: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(builder: (_) => const SrivariSevaScreen()),
                            );
                          },
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      Expanded(
                        child: QuickActionButton(
                          title: isTe ? "వసతి & గదులు" : "Accommodation",
                          subtitle: isTe ? "కాటేజీలు, రూల్స్" : "Cottages & Rules",
                          icon: Icons.hotel,
                          iconColor: const Color(0xFF2E7D32),
                          onTap: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(builder: (_) => const AccommodationScreen()),
                            );
                          },
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: QuickActionButton(
                          title: isTe ? "ఉత్సవాలు" : "Festivals",
                          subtitle: isTe ? "బ్రహ్మోత్సవాలు" : "Brahmotsavam",
                          icon: Icons.celebration,
                          iconColor: const Color(0xFF9C27B0),
                          onTap: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(builder: (_) => const FestivalsScreen()),
                            );
                          },
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),

            const SizedBox(height: 24),

            // Latest TTD Announcements Section Header
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    isTe ? "తాజా అధికారిక ప్రకటనలు" : "Latest TTD Announcements",
                    style: GoogleFonts.cinzel(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: AppTheme.maroonPrimary,
                    ),
                  ),
                  TextButton(
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (_) => const AnnouncementsScreen()),
                      );
                    },
                    child: Text(
                      isTe ? "అన్నీ చూడండి ↗" : "View All ↗",
                      style: const TextStyle(color: AppTheme.maroonPrimary, fontWeight: FontWeight.bold),
                    ),
                  ),
                ],
              ),
            ),

            // Announcements List
            if (annProvider.isLoading)
              const Center(
                child: Padding(
                  padding: EdgeInsets.all(24.0),
                  child: CircularProgressIndicator(color: AppTheme.maroonPrimary),
                ),
              )
            else if (annProvider.announcements.isEmpty)
              Center(
                child: Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Text(
                    isTe ? "ప్రకటనలు లోడ్ అవుతున్నాయి..." : "Loading official announcements...",
                    style: const TextStyle(color: AppTheme.textMuted),
                  ),
                ),
              )
            else
              ...annProvider.announcements.take(4).map(
                    (a) => AnnouncementCard(
                      announcement: a,
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (_) => AnnouncementDetailScreen(announcement: a)),
                        );
                      },
                    ),
                  ),

            const SizedBox(height: 12),
            const DisclaimerBanner(),
            const SizedBox(height: 24),
          ],
        ),
      ),
    );
  }

  Widget _statusMetric(String label, String value, IconData icon) {
    return Column(
      children: [
        Icon(icon, color: AppTheme.goldLight, size: 20),
        const SizedBox(height: 4),
        Text(
          value,
          style: const TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.bold,
            fontSize: 13,
          ),
        ),
        const SizedBox(height: 2),
        Text(
          label,
          style: const TextStyle(
            color: Colors.white70,
            fontSize: 11,
          ),
        ),
      ],
    );
  }
}

