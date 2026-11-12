import 'package:speech_to_text/speech_to_text.dart' as stt;

class STTService {
  final stt.SpeechToText _speech = stt.SpeechToText();
  bool _isAvailable = false;

  bool get isAvailable => _isAvailable;
  bool get isListening => _speech.isListening;

  Future<bool> initialize() async {
    try {
      _isAvailable = await _speech.initialize();
      return _isAvailable;
    } catch (_) {
      _isAvailable = false;
      return false;
    }
  }

  Future<void> startListening({
    required Function(String recognizedWords) onResult,
    required String lang,
  }) async {
    if (!_isAvailable) {
      await initialize();
    }

    final localeId = lang == 'te' ? 'te_IN' : 'en_IN';
    await _speech.listen(
      onResult: (val) {
        onResult(val.recognizedWords);
      },
      localeId: localeId,
      listenFor: const Duration(seconds: 25),
      pauseFor: const Duration(seconds: 4),
    );
  }

  Future<void> stopListening() async {
    await _speech.stop();
  }
}

