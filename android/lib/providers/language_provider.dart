import 'package:flutter/material.dart';
import '../services/storage_service.dart';

class LanguageProvider extends ChangeNotifier {
  final StorageService _storageService = StorageService();
  String _currentLanguage = 'te'; // Default Telugu

  String get currentLanguage => _currentLanguage;
  bool get isTelugu => _currentLanguage == 'te';

  LanguageProvider() {
    _loadLanguage();
  }

  Future<void> _loadLanguage() async {
    _currentLanguage = await _storageService.getLanguage();
    notifyListeners();
  }

  Future<void> setLanguage(String lang) async {
    if (_currentLanguage != lang) {
      _currentLanguage = lang;
      await _storageService.setLanguage(lang);
      notifyListeners();
    }
  }

  void toggleLanguage() {
    setLanguage(_currentLanguage == 'te' ? 'en' : 'te');
  }
}

