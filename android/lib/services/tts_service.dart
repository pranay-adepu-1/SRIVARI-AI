import 'package:flutter_tts/flutter_tts.dart';

class TTSService {
  final FlutterTts _flutterTts = FlutterTts();
  bool _isPlaying = false;

  bool get isPlaying => _isPlaying;

  TTSService() {
    _initTts();
  }

  void _initTts() {
    _flutterTts.setStartHandler(() {
      _isPlaying = true;
    });

    _flutterTts.setCompletionHandler(() {
      _isPlaying = false;
    });

    _flutterTts.setErrorHandler((msg) {
      _isPlaying = false;
    });
  }

  Future<void> speak(String text, String lang) async {
    if (_isPlaying) {
      await stop();
    }
    // Set appropriate language code
    final ttsLang = lang == 'te' ? 'te-IN' : 'en-IN';
    await _flutterTts.setLanguage(ttsLang);
    await _flutterTts.setPitch(1.0);
    await _flutterTts.setSpeechRate(0.85); // Gentle, reverent pace
    await _flutterTts.speak(text);
  }

  Future<void> stop() async {
    await _flutterTts.stop();
    _isPlaying = false;
  }
}

