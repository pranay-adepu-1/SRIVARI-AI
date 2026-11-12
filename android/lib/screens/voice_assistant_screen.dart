import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import '../providers/chat_provider.dart';
import '../providers/language_provider.dart';
import '../utils/theme.dart';
import '../widgets/language_switch_button.dart';

class VoiceAssistantScreen extends StatefulWidget {
  const VoiceAssistantScreen({super.key});

  @override
  State<VoiceAssistantScreen> createState() => _VoiceAssistantScreenState();
}

class _VoiceAssistantScreenState extends State<VoiceAssistantScreen> with SingleTickerProviderStateMixin {
  late AnimationController _pulseController;
  String _recognizedText = "";
  String _latestAnswer = "";

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1200),
    )..repeat(reverse: true);
  }

  @override
  void dispose() {
    _pulseController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final chatProvider = Provider.of<ChatProvider>(context);
    final langProvider = Provider.of<LanguageProvider>(context);
    final isTe = langProvider.isTelugu;

    return Scaffold(
      backgroundColor: AppTheme.creamBg,
      appBar: AppBar(
        title: Text(
          isTe ? "శ్రీవారి వాయిస్ అసిస్టెంట్" : "Srivari Voice Assistant",
          style: GoogleFonts.cinzel(fontSize: 16, fontWeight: FontWeight.bold),
        ),
        actions: const [
          Padding(
            padding: EdgeInsets.only(right: 12.0),
            child: LanguageSwitchButton(),
          ),
        ],
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 20),
          child: Column(
            children: [
              Text(
                "॥ ఓం నమో వేంకటేశాయ ॥",
                style: GoogleFonts.cinzel(
                  fontSize: 14,
                  fontWeight: FontWeight.bold,
                  color: AppTheme.goldDark,
                  letterSpacing: 1.5,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                isTe
                    ? "మీ గొంతుతో దర్శనం లేదా సేవల గురించి అడగండి"
                    : "Speak your questions about Darshan or Seva",
                style: GoogleFonts.plusJakartaSans(
                  fontSize: 14,
                  color: AppTheme.textMuted,
                ),
                textAlign: TextAlign.center,
              ),

              const Spacer(),

              // Animated Pulsing Microphone Button
              Center(
                child: GestureDetector(
                  onTap: () {
                    if (chatProvider.isListening) {
                      chatProvider.stopVoiceListening();
                    } else {
                      setState(() {
                        _recognizedText = "";
                        _latestAnswer = "";
                      });
                      chatProvider.startVoiceListening(
                        langProvider.currentLanguage,
                        (spoken) async {
                          setState(() => _recognizedText = spoken);
                          await chatProvider.sendMessage(spoken, langProvider.currentLanguage, isVoice: true);
                          if (chatProvider.messages.isNotEmpty) {
                            setState(() {
                              _latestAnswer = chatProvider.messages.last.content;
                            });
                          }
                        },
                      );
                    }
                  },
                  child: AnimatedBuilder(
                    animation: _pulseController,
                    builder: (context, child) {
                      final scale = chatProvider.isListening ? 1.0 + (_pulseController.value * 0.15) : 1.0;
                      return Transform.scale(
                        scale: scale,
                        child: Container(
                          width: 140,
                          height: 140,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            gradient: const LinearGradient(
                              colors: [AppTheme.maroonLight, AppTheme.maroonDeep],
                              begin: Alignment.topLeft,
                              end: Alignment.bottomRight,
                            ),
                            border: Border.all(
                              color: chatProvider.isListening ? Colors.redAccent : AppTheme.goldPrimary,
                              width: 3,
                            ),
                            boxShadow: [
                              BoxShadow(
                                color: (chatProvider.isListening ? Colors.red : AppTheme.goldPrimary).withOpacity(0.35),
                                blurRadius: 28,
                                spreadRadius: 6,
                              ),
                            ],
                          ),
                          child: Icon(
                            chatProvider.isListening ? Icons.mic : Icons.mic_none,
                            size: 64,
                            color: Colors.white,
                          ),
                        ),
                      );
                    },
                  ),
                ),
              ),

              const SizedBox(height: 24),

              Text(
                chatProvider.isListening
                    ? (isTe ? "మీ మాట వింటున్నాను... మాట్లాడండి" : "Listening... Speak now")
                    : (isTe ? "మాట్లాడటానికి మైక్ నొక్కండి" : "Tap microphone to speak"),
                style: GoogleFonts.plusJakartaSans(
                  fontSize: 14,
                  fontWeight: FontWeight.bold,
                  color: chatProvider.isListening ? Colors.red : AppTheme.maroonPrimary,
                ),
              ),

              const Spacer(),

              // Voice Query Result Card
              if (_recognizedText.isNotEmpty || chatProvider.isTyping || _latestAnswer.isNotEmpty)
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(18),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(14),
                    border: Border.all(color: AppTheme.borderLight),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.04),
                        blurRadius: 8,
                        offset: const Offset(0, 3),
                      )
                    ],
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      if (_recognizedText.isNotEmpty) ...[
                        Row(
                          children: [
                            const Icon(Icons.record_voice_over, size: 16, color: AppTheme.goldDark),
                            const SizedBox(width: 6),
                            Text(
                              isTe ? "మీ ప్రశ్న:" : "You asked:",
                              style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: AppTheme.textMuted),
                            ),
                          ],
                        ),
                        const SizedBox(height: 4),
                        Text(
                          _recognizedText,
                          style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
                        ),
                        const Divider(height: 20),
                      ],
                      if (chatProvider.isTyping) ...[
                        Row(
                          children: [
                            const SizedBox(
                              width: 14,
                              height: 14,
                              child: CircularProgressIndicator(strokeWidth: 2, color: AppTheme.maroonPrimary),
                            ),
                            const SizedBox(width: 8),
                            Text(
                              isTe ? "సమాధానాన్ని సిద్ధం చేస్తోంది..." : "Consulting official records...",
                              style: const TextStyle(fontSize: 12, fontStyle: FontStyle.italic),
                            ),
                          ],
                        ),
                      ] else if (_latestAnswer.isNotEmpty) ...[
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(
                              "శ్రీవారి AI (Srivari AI):",
                              style: GoogleFonts.cinzel(fontWeight: FontWeight.bold, fontSize: 13, color: AppTheme.maroonPrimary),
                            ),
                            IconButton(
                              icon: Icon(
                                chatProvider.isSpeaking ? Icons.volume_off : Icons.volume_up,
                                color: AppTheme.goldDark,
                                size: 20,
                              ),
                              onPressed: () {
                                if (chatProvider.isSpeaking) {
                                  chatProvider.stopSpeaking();
                                } else {
                                  chatProvider.speakMessage(_latestAnswer, langProvider.currentLanguage);
                                }
                              },
                              constraints: const BoxConstraints(),
                              padding: EdgeInsets.zero,
                            ),
                          ],
                        ),
                        const SizedBox(height: 6),
                        Text(
                          _latestAnswer,
                          style: const TextStyle(fontSize: 13, height: 1.4, color: AppTheme.textDark),
                          maxLines: 6,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ],
                    ],
                  ),
                ),

              const SizedBox(height: 16),
            ],
          ),
        ),
      ),
    );
  }
}

