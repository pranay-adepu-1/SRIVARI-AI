import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import 'package:share_plus/share_plus.dart';
import '../models/announcement.dart';
import '../providers/language_provider.dart';
import '../providers/announcement_provider.dart';
import '../utils/theme.dart';
import '../utils/date_formatter.dart';
import 'status_badge.dart';

class AnnouncementCard extends StatelessWidget {
  final Announcement announcement;
  final VoidCallback onTap;

  const AnnouncementCard({
    super.key,
    required this.announcement,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final lang = Provider.of<LanguageProvider>(context).currentLanguage;
    final annProvider = Provider.of<AnnouncementProvider>(context, listen: false);

    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      elevation: 1.5,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(14),
        side: const BorderSide(color: AppTheme.borderLight, width: 0.8),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(14),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Row(
                    children: [
                      if (announcement.isQuotaAlert) ...[
                        StatusBadge.quotaAlert(),
                        const SizedBox(width: 8),
                      ],
                      if (announcement.isVerified) StatusBadge.verified(),
                    ],
                  ),
                  Row(
                    children: [
                      IconButton(
                        icon: Icon(
                          announcement.isBookmarked ? Icons.bookmark : Icons.bookmark_border,
                          color: announcement.isBookmarked ? AppTheme.maroonPrimary : AppTheme.textMuted,
                          size: 20,
                        ),
                        onPressed: () {
                          annProvider.toggleBookmark(announcement);
                        },
                        constraints: const BoxConstraints(),
                        padding: EdgeInsets.zero,
                      ),
                      const SizedBox(width: 12),
                      IconButton(
                        icon: const Icon(Icons.share, color: AppTheme.textMuted, size: 18),
                        onPressed: () {
                          Share.share(
                            "${announcement.getTitle(lang)}\n\n${announcement.getContent(lang)}\n\nSource: ${announcement.sourceUrl}",
                          );
                        },
                        constraints: const BoxConstraints(),
                        padding: EdgeInsets.zero,
                      ),
                    ],
                  )
                ],
              ),
              const SizedBox(height: 10),
              Text(
                announcement.getTitle(lang),
                style: GoogleFonts.plusJakartaSans(
                  fontWeight: FontWeight.bold,
                  fontSize: 15,
                  color: AppTheme.textDark,
                  height: 1.3,
                ),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
              const SizedBox(height: 6),
              Text(
                announcement.getContent(lang),
                style: GoogleFonts.plusJakartaSans(
                  fontSize: 13,
                  color: AppTheme.textMuted,
                  height: 1.4,
                ),
                maxLines: 3,
                overflow: TextOverflow.ellipsis,
              ),
              const SizedBox(height: 12),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Row(
                    children: [
                      const Icon(Icons.access_time, size: 12, color: AppTheme.textMuted),
                      const SizedBox(width: 4),
                      Text(
                        DateFormatter.timeAgo(announcement.publicationDate, lang),
                        style: const TextStyle(fontSize: 11, color: AppTheme.textMuted),
                      ),
                    ],
                  ),
                  Row(
                    children: [
                      Text(
                        announcement.sourceDomain,
                        style: const TextStyle(
                          fontSize: 11,
                          color: AppTheme.maroonPrimary,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                      const SizedBox(width: 4),
                      const Icon(Icons.open_in_new, size: 12, color: AppTheme.maroonPrimary),
                    ],
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}

