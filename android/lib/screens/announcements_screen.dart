import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import '../providers/announcement_provider.dart';
import '../providers/language_provider.dart';
import '../utils/theme.dart';
import '../widgets/announcement_card.dart';
import 'announcement_detail_screen.dart';

class AnnouncementsScreen extends StatefulWidget {
  const AnnouncementsScreen({super.key});

  @override
  State<AnnouncementsScreen> createState() => _AnnouncementsScreenState();
}

class _AnnouncementsScreenState extends State<AnnouncementsScreen> {
  final TextEditingController _searchController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    final annProvider = Provider.of<AnnouncementProvider>(context);
    final lang = Provider.of<LanguageProvider>(context).currentLanguage;
    final isTe = lang == 'te';

    return Scaffold(
      appBar: AppBar(
        title: Text(
          isTe ? "అధికారిక టీటీడీ ప్రకటనలు" : "Official TTD Announcements",
          style: GoogleFonts.cinzel(fontSize: 17, fontWeight: FontWeight.bold),
        ),
      ),
      body: Column(
        children: [
          // Search Bar
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: TextField(
              controller: _searchController,
              decoration: InputDecoration(
                hintText: isTe ? "ప్రకటనలను వెతకండి..." : "Search official announcements...",
                prefixIcon: const Icon(Icons.search, color: AppTheme.maroonPrimary),
                suffixIcon: _searchController.text.isNotEmpty
                    ? IconButton(
                        icon: const Icon(Icons.clear),
                        onPressed: () {
                          _searchController.clear();
                          annProvider.setSearchQuery('');
                        },
                      )
                    : null,
                filled: true,
                fillColor: Colors.white,
                contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: const BorderSide(color: AppTheme.borderLight),
                ),
              ),
              onChanged: (val) {
                annProvider.setSearchQuery(val.trim());
              },
            ),
          ),

          // Category Chips Horizontal List
          SizedBox(
            height: 38,
            child: ListView(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.symmetric(horizontal: 16),
              children: [
                _categoryChip(
                  label: isTe ? "అన్నీ (All)" : "All",
                  isSelected: annProvider.selectedCategorySlug == 'all',
                  onTap: () => annProvider.selectCategory('all'),
                ),
                ...annProvider.categories.map(
                  (c) => _categoryChip(
                    label: c.getName(lang),
                    isSelected: annProvider.selectedCategorySlug == c.slug,
                    onTap: () => annProvider.selectCategory(c.slug),
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: 8),

          // Announcements List
          Expanded(
            child: RefreshIndicator(
              onRefresh: () => annProvider.loadAnnouncements(),
              color: AppTheme.maroonPrimary,
              child: annProvider.isLoading
                  ? const Center(child: CircularProgressIndicator(color: AppTheme.maroonPrimary))
                  : annProvider.announcements.isEmpty
                      ? Center(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              const Icon(Icons.campaign_outlined, size: 48, color: AppTheme.textMuted),
                              const SizedBox(height: 12),
                              Text(
                                isTe ? "ఎలాంటి ప్రకటనలు లభించలేదు" : "No announcements found",
                                style: const TextStyle(color: AppTheme.textMuted),
                              ),
                            ],
                          ),
                        )
                      : ListView.builder(
                          padding: const EdgeInsets.only(top: 8, bottom: 20),
                          itemCount: annProvider.announcements.length,
                          itemBuilder: (context, index) {
                            final item = annProvider.announcements[index];
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
            ),
          ),
        ],
      ),
    );
  }

  Widget _categoryChip({
    required String label,
    required bool isSelected,
    required VoidCallback onTap,
  }) {
    return Padding(
      padding: const EdgeInsets.only(right: 8.0),
      child: FilterChip(
        label: Text(
          label,
          style: TextStyle(
            fontSize: 12,
            fontWeight: FontWeight.bold,
            color: isSelected ? Colors.white : AppTheme.textDark,
          ),
        ),
        selected: isSelected,
        onSelected: (_) => onTap(),
        selectedColor: AppTheme.maroonPrimary,
        backgroundColor: Colors.white,
        side: BorderSide(color: isSelected ? AppTheme.maroonPrimary : AppTheme.borderLight),
        checkmarkColor: Colors.white,
      ),
    );
  }
}

