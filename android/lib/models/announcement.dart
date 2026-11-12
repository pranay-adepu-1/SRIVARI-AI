class Announcement {
  final String id;
  final String? categoryId;
  final String titleEn;
  final String titleTe;
  final String contentEn;
  final String contentTe;
  final String sourceUrl;
  final String sourceDomain;
  final DateTime publicationDate;
  final bool isVerified;
  final bool isQuotaAlert;
  final DateTime? quotaDate;
  bool isBookmarked;

  Announcement({
    required this.id,
    this.categoryId,
    required this.titleEn,
    required this.titleTe,
    required this.contentEn,
    required this.contentTe,
    required this.sourceUrl,
    required this.sourceDomain,
    required this.publicationDate,
    required this.isVerified,
    required this.isQuotaAlert,
    this.quotaDate,
    this.isBookmarked = false,
  });

  String getTitle(String lang) => lang == 'te' ? titleTe : titleEn;
  String getContent(String lang) => lang == 'te' ? contentTe : contentEn;

  factory Announcement.fromJson(Map<String, dynamic> json) {
    return Announcement(
      id: json['id'] ?? '',
      categoryId: json['category_id'],
      titleEn: json['title_en'] ?? '',
      titleTe: json['title_te'] ?? json['title_en'] ?? '',
      contentEn: json['content_en'] ?? '',
      contentTe: json['content_te'] ?? json['content_en'] ?? '',
      sourceUrl: json['source_url'] ?? '',
      sourceDomain: json['source_domain'] ?? 'news.tirumala.org',
      publicationDate: DateTime.tryParse(json['publication_date'] ?? '') ?? DateTime.now(),
      isVerified: json['is_verified'] ?? true,
      isQuotaAlert: json['is_quota_alert'] ?? false,
      quotaDate: json['quota_date'] != null ? DateTime.tryParse(json['quota_date']) : null,
      isBookmarked: json['is_bookmarked'] ?? false,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'category_id': categoryId,
      'title_en': titleEn,
      'title_te': titleTe,
      'content_en': contentEn,
      'content_te': contentTe,
      'source_url': sourceUrl,
      'source_domain': sourceDomain,
      'publication_date': publicationDate.toIso8601String(),
      'is_verified': isVerified,
      'is_quota_alert': isQuotaAlert,
      'quota_date': quotaDate?.toIso8601String(),
      'is_bookmarked': isBookmarked,
    };
  }
}

