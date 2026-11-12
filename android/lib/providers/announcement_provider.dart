import 'package:flutter/material.dart';
import '../models/announcement.dart';
import '../models/category.dart';
import '../services/api_service.dart';
import '../services/storage_service.dart';

class AnnouncementProvider extends ChangeNotifier {
  final ApiService _apiService = ApiService();
  final StorageService _storageService = StorageService();

  List<Announcement> _announcements = [];
  List<AnnouncementCategoryItem> _categories = [];
  List<Announcement> _bookmarks = [];
  String _selectedCategorySlug = 'all';
  String _searchQuery = '';
  bool _isLoading = false;

  List<Announcement> get announcements => _announcements;
  List<AnnouncementCategoryItem> get categories => _categories;
  List<Announcement> get bookmarks => _bookmarks;
  String get selectedCategorySlug => _selectedCategorySlug;
  bool get isLoading => _isLoading;

  AnnouncementProvider() {
    loadCategories();
    loadAnnouncements();
    loadLocalBookmarks();
  }

  Future<void> loadCategories() async {
    _categories = await _apiService.getCategories();
    notifyListeners();
  }

  Future<void> loadAnnouncements() async {
    _isLoading = true;
    notifyListeners();

    _announcements = await _apiService.getAnnouncements(
      categorySlug: _selectedCategorySlug,
      search: _searchQuery,
    );

    // Merge bookmark state
    final bookmarkedIds = _bookmarks.map((b) => b.id).toSet();
    for (var a in _announcements) {
      if (bookmarkedIds.contains(a.id)) {
        a.isBookmarked = true;
      }
    }

    _isLoading = false;
    notifyListeners();
  }

  void selectCategory(String slug) {
    if (_selectedCategorySlug != slug) {
      _selectedCategorySlug = slug;
      loadAnnouncements();
    }
  }

  void setSearchQuery(String query) {
    _searchQuery = query;
    loadAnnouncements();
  }

  Future<void> loadLocalBookmarks() async {
    _bookmarks = await _storageService.getLocalBookmarks();
    notifyListeners();
  }

  Future<void> toggleBookmark(Announcement announcement) async {
    announcement.isBookmarked = !announcement.isBookmarked;

    if (announcement.isBookmarked) {
      if (!_bookmarks.any((b) => b.id == announcement.id)) {
        _bookmarks.add(announcement);
      }
    } else {
      _bookmarks.removeWhere((b) => b.id == announcement.id);
    }

    await _storageService.saveLocalBookmarks(_bookmarks);
    _apiService.toggleBookmark(announcement.id);
    notifyListeners();
  }
}

