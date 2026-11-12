class DevoteeUser {
  final String id;
  final String? email;
  final String? phoneNumber;
  final String deviceId;
  final String preferredLanguage;
  final int bookmarksCount;

  DevoteeUser({
    required this.id,
    this.email,
    this.phoneNumber,
    required this.deviceId,
    required this.preferredLanguage,
    this.bookmarksCount = 0,
  });

  factory DevoteeUser.fromJson(Map<String, dynamic> json) {
    return DevoteeUser(
      id: json['id'] ?? '',
      email: json['email'],
      phoneNumber: json['phone_number'],
      deviceId: json['device_id'] ?? '',
      preferredLanguage: json['preferred_language'] ?? 'te',
      bookmarksCount: json['bookmarks_count'] ?? 0,
    );
  }
}

