import 'dart:convert';
import 'package:http/http.dart' as http;
import '../utils/constants.dart';
import '../models/announcement.dart';
import '../models/category.dart';
import '../models/darshan_info.dart';
import '../models/accommodation_info.dart';
import '../models/notification_item.dart';

class ApiService {
  final String baseUrl;
  String? authToken;

  ApiService({this.baseUrl = AppConstants.apiBaseUrl});

  void setToken(String token) {
    authToken = token;
  }

  Map<String, String> get _headers => {
        'Content-Type': 'application/json',
        if (authToken != null) 'Authorization': 'Bearer $authToken',
      };

  // Auth: Devotee Handshake
  Future<Map<String, dynamic>> devoteeInit(String deviceId, String preferredLanguage, {String? fcmToken}) async {
    try {
      final res = await http.post(
        Uri.parse('$baseUrl/auth/devotee-init'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'device_id': deviceId,
          'preferred_language': preferredLanguage,
          'fcm_token': fcmToken,
        }),
      ).timeout(const Duration(seconds: 10));

      if (res.statusCode == 200) {
        return jsonDecode(res.body);
      }
    } catch (_) {}
    return {
      'user_id': 'local_user',
      'access_token': 'offline_token',
      'preferred_language': preferredLanguage,
    };
  }

  // Announcements
  Future<List<Announcement>> getAnnouncements({String? categorySlug, String? search}) async {
    try {
      String query = '$baseUrl/announcements?limit=50';
      if (categorySlug != null && categorySlug != 'all') query += '&category=$categorySlug';
      if (search != null && search.isNotEmpty) query += '&search=${Uri.encodeComponent(search)}';

      final res = await http.get(Uri.parse(query), headers: _headers).timeout(const Duration(seconds: 10));
      if (res.statusCode == 200) {
        final data = jsonDecode(res.body);
        final List items = data['items'] ?? [];
        return items.map((a) => Announcement.fromJson(a)).toList();
      }
    } catch (_) {}
    return [];
  }

  // Categories
  Future<List<AnnouncementCategoryItem>> getCategories() async {
    try {
      final res = await http.get(Uri.parse('$baseUrl/announcements/categories'), headers: _headers);
      if (res.statusCode == 200) {
        final List list = jsonDecode(res.body);
        return list.map((c) => AnnouncementCategoryItem.fromJson(c)).toList();
      }
    } catch (_) {}
    return [];
  }

  // AI Chat Query
  Future<Map<String, dynamic>> askQuestion(String query, {String? sessionId, String? language, bool isVoice = false}) async {
    try {
      final res = await http.post(
        Uri.parse('$baseUrl/chat/query'),
        headers: _headers,
        body: jsonEncode({
          'query': query,
          'session_id': sessionId,
          'language': language,
          'is_voice': isVoice,
        }),
      ).timeout(const Duration(seconds: 15));

      if (res.statusCode == 200) {
        return jsonDecode(res.body);
      }
    } catch (_) {}

    // Offline / fallback response
    final isTe = language == 'te';
    return {
      'answer': isTe
          ? 'ఓం నమో వేంకటేశాయ! దర్శనం మరియు సేవల కోసం అధికారిక వెబ్‌సైట్ https://ttdevasthanams.ap.gov.in/ మాత్రమే ఉపయోగించండి.'
          : 'Om Namo Venkatesaya! Please visit the official TTD portal https://ttdevasthanams.ap.gov.in/ for verified booking details.',
      'language': isTe ? 'te' : 'en',
      'is_verified': true,
      'citations': [
        {
          'title': 'Official TTD Portal',
          'url': AppConstants.ttdBookingPortal,
          'source': 'ttdevasthanams.ap.gov.in',
        }
      ],
      'suggested_questions': [],
    };
  }

  // Darshan Guides
  Future<List<DarshanGuideItem>> getDarshanGuides() async {
    try {
      final res = await http.get(Uri.parse('$baseUrl/darshan/guides'), headers: _headers);
      if (res.statusCode == 200) {
        final List list = jsonDecode(res.body);
        return list.map((d) => DarshanGuideItem.fromJson(d)).toList();
      }
    } catch (_) {}
    return [];
  }

  // Accommodation Guides
  Future<List<AccommodationGuideItem>> getAccommodationGuides() async {
    try {
      final res = await http.get(Uri.parse('$baseUrl/accommodation/guides'), headers: _headers);
      if (res.statusCode == 200) {
        final List list = jsonDecode(res.body);
        return list.map((a) => AccommodationGuideItem.fromJson(a)).toList();
      }
    } catch (_) {}
    return [];
  }

  // Notifications
  Future<List<NotificationItem>> getNotificationHistory() async {
    try {
      final res = await http.get(Uri.parse('$baseUrl/notifications/history'), headers: _headers);
      if (res.statusCode == 200) {
        final List list = jsonDecode(res.body);
        return list.map((n) => NotificationItem.fromJson(n)).toList();
      }
    } catch (_) {}
    return [];
  }

  // Toggle Bookmark
  Future<bool> toggleBookmark(String announcementId) async {
    try {
      final res = await http.post(Uri.parse('$baseUrl/announcements/$announcementId/bookmark'), headers: _headers);
      if (res.statusCode == 200) {
        final data = jsonDecode(res.body);
        return data['is_bookmarked'] ?? false;
      }
    } catch (_) {}
    return false;
  }
}

