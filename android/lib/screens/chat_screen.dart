import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import '../providers/chat_provider.dart';
import '../providers/language_provider.dart';
import '../utils/theme.dart';
import '../widgets/chat_bubble.dart';
import '../widgets/language_switch_button.dart';

class ChatScreen extends StatefulWidget {
  final String? initialQuery;

  const ChatScreen({super.key, this.initialQuery});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _textController = TextEditingController();
  final ScrollController _scrollController = ScrollController();

  @override
  void initState() {
    super.initState();
    if (widget.initialQuery != null) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        final lang = Provider.of<LanguageProvider>(context, listen: false).currentLanguage;
        Provider.of<ChatProvider>(context, listen: false).sendMessage(widget.initialQuery!, lang);
      });
    }
  }

  void _scrollToBottom() {
    if (_scrollController.hasClients) {
      _scrollController.animateTo(
        _scrollController.position.maxScrollExtent + 80,
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeOut,
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final chatProvider = Provider.of<ChatProvider>(context);
    final langProvider = Provider.of<LanguageProvider>(context);
    final isTe = langProvider.isTelugu;

    return Scaffold(
      appBar: AppBar(
        title: Column(
          children: [
            Text(
              isTe ? "శ్రీవారి AI సహాయకుడు" : "Srivari AI Assistant",
              style: GoogleFonts.cinzel(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            Text(
              "॥ ఓం నమో వేంకటేశాయ ॥",
              style: TextStyle(fontSize: 11, color: AppTheme.goldLight.withOpacity(0.9)),
            ),
          ],
        ),
        actions: const [
          Padding(
            padding: EdgeInsets.only(right: 12.0),
            child: LanguageSwitchButton(),
          )
        ],
      ),
      body: Column(
        children: [
          // Informational Warning Banner
          Container(
            width: double.infinity,
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
            color: const Color(0xFFFFF9E6),
            child: Row(
              children: [
                const Icon(Icons.verified_user, size: 14, color: AppTheme.goldDark),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    isTe
                        ? "అధికారిక టీటీడీ సమాచారం ఆధారంగా సమాధానాలు ఇవ్వబడతాయి."
                        : "Answers cited strictly from official TTD channels.",
                    style: const TextStyle(fontSize: 11, color: AppTheme.textDark),
                  ),
                ),
              ],
            ),
          ),

          // Messages List
          Expanded(
            child: chatProvider.messages.isEmpty
                ? _buildEmptyState(isTe, chatProvider)
                : ListView.builder(
                    controller: _scrollController,
                    padding: const EdgeInsets.symmetric(vertical: 12),
                    itemCount: chatProvider.messages.length,
                    itemBuilder: (context, index) {
                      return ChatBubble(message: chatProvider.messages[index]);
                    },
                  ),
          ),

          // Typing Indicator
          if (chatProvider.isTyping)
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
              child: Row(
                children: [
                  const SizedBox(
                    width: 16,
                    height: 16,
                    child: CircularProgressIndicator(strokeWidth: 2, color: AppTheme.maroonPrimary),
                  ),
                  const SizedBox(width: 10),
                  Text(
                    isTe ? "శ్రీవారి AI సమాధానాన్ని సిద్ధం చేస్తోంది..." : "Srivari AI is consulting official records...",
                    style: const TextStyle(fontSize: 12, color: AppTheme.textMuted, fontStyle: FontStyle.italic),
                  ),
                ],
              ),
            ),

          // Suggested Questions Carousel
          if (chatProvider.suggestedQuestions.isNotEmpty)
            SizedBox(
              height: 40,
              child: ListView.builder(
                scrollDirection: Axis.horizontal,
                padding: const EdgeInsets.symmetric(horizontal: 12),
                itemCount: chatProvider.suggestedQuestions.length,
                itemBuilder: (context, index) {
                  final prompt = chatProvider.suggestedQuestions[index];
                  return Padding(
                    padding: const EdgeInsets.only(right: 8),
                    child: ActionChip(
                      label: Text(prompt, style: const TextStyle(fontSize: 12)),
                      backgroundColor: Colors.white,
                      side: const BorderSide(color: AppTheme.borderLight),
                      onPressed: () {
                        chatProvider.sendMessage(prompt, langProvider.currentLanguage);
                        _scrollToBottom();
                      },
                    ),
                  );
                },
              ),
            ),

          const SizedBox(height: 6),

          // Input Bar
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            decoration: BoxDecoration(
              color: Colors.white,
              border: Border(top: BorderSide(color: AppTheme.borderLight.withOpacity(0.5))),
            ),
            child: SafeArea(
              child: Row(
                children: [
                  // Microphone Voice Button
                  IconButton(
                    icon: Icon(
                      chatProvider.isListening ? Icons.mic : Icons.mic_none,
                      color: chatProvider.isListening ? Colors.red : AppTheme.maroonPrimary,
                    ),
                    onPressed: () {
                      if (chatProvider.isListening) {
                        chatProvider.stopVoiceListening();
                      } else {
                        chatProvider.startVoiceListening(
                          langProvider.currentLanguage,
                          (spokenText) {
                            _textController.text = spokenText;
                            chatProvider.sendMessage(spokenText, langProvider.currentLanguage, isVoice: true);
                            _textController.clear();
                            _scrollToBottom();
                          },
                        );
                      }
                    },
                  ),

                  // Text Field
                  Expanded(
                    child: TextField(
                      controller: _textController,
                      decoration: InputDecoration(
                        hintText: isTe ? "మీ ప్రశ్నను అడగండి..." : "Ask your question...",
                        hintStyle: const TextStyle(fontSize: 14, color: AppTheme.textMuted),
                        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(24),
                          borderSide: const BorderSide(color: AppTheme.borderLight),
                        ),
                        focusedBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(24),
                          borderSide: const BorderSide(color: AppTheme.goldPrimary),
                        ),
                        filled: true,
                        fillColor: AppTheme.creamBg,
                      ),
                      onSubmitted: (val) {
                        if (val.trim().isNotEmpty) {
                          chatProvider.sendMessage(val, langProvider.currentLanguage);
                          _textController.clear();
                          _scrollToBottom();
                        }
                      },
                    ),
                  ),

                  const SizedBox(width: 6),

                  // Send Button
                  IconButton(
                    icon: const Icon(Icons.send_rounded, color: AppTheme.maroonPrimary),
                    onPressed: () {
                      final text = _textController.text.trim();
                      if (text.isNotEmpty) {
                        chatProvider.sendMessage(text, langProvider.currentLanguage);
                        _textController.clear();
                        _scrollToBottom();
                      }
                    },
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildEmptyState(bool isTe, ChatProvider chatProvider) {
    return Center(
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(28),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              width: 72,
              height: 72,
              decoration: BoxDecoration(
                color: AppTheme.maroonPrimary.withOpacity(0.08),
                shape: BoxShape.circle,
                border: Border.all(color: AppTheme.goldPrimary),
              ),
              child: const Icon(Icons.psychology, size: 36, color: AppTheme.maroonPrimary),
            ),
            const SizedBox(height: 16),
            Text(
              isTe ? "శ్రీవారి AI సహాయకుడు" : "Srivari AI Devotee Assistant",
              style: GoogleFonts.cinzel(fontSize: 20, fontWeight: FontWeight.bold, color: AppTheme.maroonPrimary),
            ),
            const SizedBox(height: 8),
            Text(
              isTe
                  ? "ఓం నమో వేంకటేశాయ! దర్శనం, సేవలు, వసతి మరియు టీటీడీ నియమాల గురించి నన్ను అడగండి."
                  : "Om Namo Venkatesaya! Ask me about Darshan, Srivari Seva, cottages, waiting times, or rules.",
              style: const TextStyle(fontSize: 13, color: AppTheme.textMuted),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 24),
            Text(
              isTe ? "తరచుగా అడిగే ప్రశ్నలు:" : "Frequently Asked Questions:",
              style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: AppTheme.textDark),
            ),
            const SizedBox(height: 12),
            ...chatProvider.suggestedQuestions.map(
              (q) => Padding(
                padding: const EdgeInsets.symmetric(vertical: 4.0),
                child: InkWell(
                  onTap: () {
                    final lang = Provider.of<LanguageProvider>(context, listen: false).currentLanguage;
                    chatProvider.sendMessage(q, lang);
                  },
                  borderRadius: BorderRadius.circular(8),
                  child: Container(
                    width: double.infinity,
                    padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      border: Border.all(color: AppTheme.borderLight),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Text(
                      q,
                      style: const TextStyle(fontSize: 13, color: AppTheme.maroonPrimary),
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

