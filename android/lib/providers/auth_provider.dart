import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../services/storage_service.dart';

class AuthProvider extends ChangeNotifier {
  final ApiService _apiService = ApiService();
  final StorageService _storageService = StorageService();

  String? _userId;
  String? _authToken;
  bool _isInitialized = false;

  String? get userId => _userId;
  String? get authToken => _authToken;
  bool get isInitialized => _isInitialized;

  Future<void> initAuth(String preferredLanguage) async {
    final deviceId = await _storageService.getDeviceId();
    final token = await _storageService.getAuthToken();

    if (token != null) {
      _authToken = token;
      _apiService.setToken(token);
    }

    final res = await _apiService.devoteeInit(deviceId, preferredLanguage);
    if (res.containsKey('access_token')) {
      _authToken = res['access_token'];
      _userId = res['user_id'];
      await _storageService.setAuthToken(_authToken!);
      _apiService.setToken(_authToken!);
    }

    _isInitialized = true;
    notifyListeners();
  }
}

