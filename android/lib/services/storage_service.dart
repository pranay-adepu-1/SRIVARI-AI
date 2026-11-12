import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/announcement.dart';

class StorageService {
  static const String _keyDeviceId = "srivari_device_id";
  static const String _keyLanguage = "srivari_language";
  static const String _keyToken = "srivari_auth_token";
  static const String _keyBookmarks = "srivari_bookmarks_cache";
  static const String _keyOnboardingDone = "srivari_onboarding_done";

  Future<String> getDeviceId() async {
    final prefs = await SharedPreferences.getInstance();
    String? id = prefs.getString(_keyDeviceId);
    if (id == null) {
      id = "dev_${DateTime.now().millisecondsSinceEpoch}_${(1000 + (DateTime.now().microsecond % 9000))}";
      await prefs.setString(_keyDeviceId, id);
    }
    return id;
  }

  Future<String> getLanguage() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_keyLanguage) ?? 'te'; // Telugu default
  }

  Future<void> setLanguage(String lang) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_keyLanguage, lang);
  }

  Future<String?> getAuthToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_keyToken);
  }

  Future<void> setAuthToken(String token) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_keyToken, token);
  }

  Future<bool> isOnboardingDone() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool(_keyOnboardingDone) ?? false;
  }

  Future<void> setOnboardingDone(bool done) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_keyOnboardingDone, done);
  }

  // Local Offline Bookmarks
  Future<List<Announcement>> getLocalBookmarks() async {
    final prefs = await SharedPreferences.getInstance();
    final String? raw = prefs.getString(_keyBookmarks);
    if (raw == null) return [];
    try {
      final List list = jsonDecode(raw);
      return list.map((a) => Announcement.fromJson(a)).toList();
    } catch (_) {
      return [];
    }
  }

  Future<void> saveLocalBookmarks(List<Announcement> bookmarks) async {
    final prefs = await SharedPreferences.getInstance();
    final raw = jsonEncode(bookmarks.map((b) => b.toJson()).toList());
    await prefs.setString(_keyBookmarks, raw);
  }
}

