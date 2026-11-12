class NotificationItem {
  final String id;
  final String? announcementId;
  final String titleEn;
  final String titleTe;
  final String bodyEn;
  final String bodyTe;
  final String notificationType;
  final DateTime sentAt;
  bool isRead;

  NotificationItem({
    required this.id,
    this.announcementId,
    required this.titleEn,
    required this.titleTe,
    required this.bodyEn,
    required this.bodyTe,
    required this.notificationType,
    required this.sentAt,
    this.isRead = false,
  });

  String getTitle(String lang) => lang == 'te' ? titleTe : titleEn;
  String getBody(String lang) => lang == 'te' ? bodyTe : bodyEn;

  factory NotificationItem.fromJson(Map<String, dynamic> json) {
    return NotificationItem(
      id: json['id'] ?? '',
      announcementId: json['announcement_id'],
      titleEn: json['title_en'] ?? '',
      titleTe: json['title_te'] ?? json['title_en'] ?? '',
      bodyEn: json['body_en'] ?? '',
      bodyTe: json['body_te'] ?? json['body_en'] ?? '',
      notificationType: json['notification_type'] ?? 'quota_alert',
      sentAt: DateTime.tryParse(json['sent_at'] ?? '') ?? DateTime.now(),
      isRead: false,
    );
  }
}

