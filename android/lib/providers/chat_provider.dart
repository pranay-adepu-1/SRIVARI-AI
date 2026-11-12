import 'package:flutter/material.dart';
import '../models/chat_message.dart';
import '../services/api_service.dart';
import '../services/tts_service.dart';
import '../services/stt_service.dart';

class ChatProvider extends ChangeNotifier {
  final ApiService _apiService = ApiService();
  final TTSService _ttsService = TTSService();
  final STTService _sttService = STTService();

  final List<ChatMessageItem> _messages = [];
  String? _sessionId;
  bool _isTyping = false;
  bool _isListening = false;
  bool _isSpeaking = false;
  List<String> _suggestedQuestions = [];

  List<ChatMessageItem> get messages => _messages;
  bool get isTyping => _isTyping;
  bool get isListening => _isListening;
  bool get isSpeaking => _isSpeaking;
  List<String> get suggestedQuestions => _suggestedQuestions;

  ChatProvider() {
    _suggestedQuestions = [
      "₹300 దర్శనం ఎలా బుక్ చేసుకోవాలి?",
      "శ్రీవారి సేవ నియమాలు ఏమిటి?",
      "తిరుమలలో రూమ్స్ బుకింగ్ విధానం",
      "సర్వ దర్శనం (ఉచితం) ఎక్కడ ఇస్తారు?"
    ];
  }

  Future<void> sendMessage(String text, String lang, {bool isVoice = false}) async {
    if (text.trim().isEmpty) return;

    final userMsg = ChatMessageItem(
      id: UniqueKey().toString(),
      sender: 'user',
      content: text,
      language: lang,
      isVoice: isVoice,
      createdAt: DateTime.now(),
    );

    _messages.add(userMsg);
    _isTyping = true;
    notifyListeners();

    final response = await _apiService.askQuestion(
      text,
      sessionId: _sessionId,
      language: lang,
      isVoice: isVoice,
    );

    _isTyping = false;
    _sessionId = response['session_id'];

    final List rawCitations = response['citations'] ?? [];
    final List<Citation> citations = rawCitations.map((c) => Citation.fromJson(c)).toList();

    final botMsg = ChatMessageItem(
      id: UniqueKey().toString(),
      sender: 'assistant',
      content: response['answer'] ?? '',
      language: response['language'] ?? lang,
      citations: citations,
      createdAt: DateTime.now(),
    );

    _messages.add(botMsg);

    if (response.containsKey('suggested_questions')) {
      _suggestedQuestions = List<String>.from(response['suggested_questions']);
    }

    notifyListeners();

    // If question was spoken, read back the answer
    if (isVoice) {
      speakMessage(botMsg.content, botMsg.language);
    }
  }

  Future<void> speakMessage(String content, String lang) async {
    _isSpeaking = true;
    notifyListeners();
    await _ttsService.speak(content, lang);
    _isSpeaking = false;
    notifyListeners();
  }

  Future<void> stopSpeaking() async {
    await _ttsService.stop();
    _isSpeaking = false;
    notifyListeners();
  }

  Future<void> startVoiceListening(String lang, Function(String) onComplete) async {
    _isListening = true;
    notifyListeners();

    await _sttService.startListening(
      lang: lang,
      onResult: (spokenText) {
        if (spokenText.isNotEmpty) {
          _isListening = false;
          notifyListeners();
          onComplete(spokenText);
        }
      },
    );
  }

  Future<void> stopVoiceListening() async {
    await _sttService.stopListening();
    _isListening = false;
    notifyListeners();
  }

  void clearChat() {
    _messages.clear();
    _sessionId = null;
    notifyListeners();
  }
}

