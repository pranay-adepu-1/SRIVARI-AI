import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import 'package:url_launcher/url_launcher.dart';
import '../models/chat_message.dart';
import '../providers/chat_provider.dart';
import '../utils/theme.dart';

class ChatBubble extends StatelessWidget {
  final ChatMessageItem message;

  const ChatBubble({super.key, required this.message});

  @override
  Widget build(BuildContext context) {
    final chatProvider = Provider.of<ChatProvider>(context, listen: false);

    if (message.isUser) {
      return Align(
        alignment: Alignment.centerRight,
        child: Container(
          margin: const EdgeInsets.only(top: 8, bottom: 8, left: 50, right: 16),
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
          decoration: BoxDecoration(
            gradient: const LinearGradient(
              colors: [AppTheme.maroonLight, AppTheme.maroonPrimary],
            ),
            borderRadius: const BorderRadius.only(
              topLeft: Radius.circular(16),
              topRight: Radius.circular(16),
              bottomLeft: Radius.circular(16),
              bottomRight: Radius.circular(4),
            ),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.06),
                blurRadius: 4,
                offset: const Offset(0, 2),
              ),
            ],
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              Text(
                message.content,
                style: GoogleFonts.plusJakartaSans(
                  color: Colors.white,
                  fontSize: 14,
                  height: 1.4,
                ),
              ),
              if (message.isVoice) ...[
                const SizedBox(height: 4),
                const Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(Icons.mic, size: 12, color: AppTheme.goldLight),
                    SizedBox(width: 4),
                    Text(
                      "Voice query",
                      style: TextStyle(color: AppTheme.goldLight, fontSize: 10),
                    )
                  ],
                ),
              ]
            ],
          ),
        ),
      );
    }

    // Bot Assistant Bubble
    return Align(
      alignment: Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.only(top: 8, bottom: 8, left: 16, right: 50),
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: const BorderRadius.only(
            topLeft: Radius.circular(16),
            topRight: Radius.circular(16),
            bottomLeft: Radius.circular(4),
            bottomRight: Radius.circular(16),
          ),
          border: Border.all(color: AppTheme.borderLight, width: 0.8),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.04),
              blurRadius: 6,
              offset: const Offset(0, 2),
            ),
          ],
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(4),
                      decoration: BoxDecoration(
                        color: AppTheme.maroonPrimary.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(6),
                      ),
                      child: const Icon(Icons.temple_hindu, size: 14, color: AppTheme.maroonPrimary),
                    ),
                    const SizedBox(width: 6),
                    Text(
                      "శ్రీవారి AI (Srivari AI)",
                      style: GoogleFonts.cinzel(
                        fontSize: 12,
                        fontWeight: FontWeight.bold,
                        color: AppTheme.maroonPrimary,
                      ),
                    ),
                  ],
                ),
                Row(
                  children: [
                    IconButton(
                      icon: const Icon(Icons.volume_up, size: 18, color: AppTheme.goldDark),
                      onPressed: () {
                        chatProvider.speakMessage(message.content, message.language);
                      },
                      constraints: const BoxConstraints(),
                      padding: EdgeInsets.zero,
                    ),
                    const SizedBox(width: 8),
                    IconButton(
                      icon: const Icon(Icons.copy, size: 16, color: AppTheme.textMuted),
                      onPressed: () {
                        Clipboard.setData(ClipboardData(text: message.content));
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text("Copied to clipboard")),
                        );
                      },
                      constraints: const BoxConstraints(),
                      padding: EdgeInsets.zero,
                    ),
                  ],
                )
              ],
            ),
            const SizedBox(height: 10),
            Text(
              message.content,
              style: GoogleFonts.plusJakartaSans(
                color: AppTheme.textDark,
                fontSize: 14,
                height: 1.5,
              ),
            ),
            if (message.citations.isNotEmpty) ...[
              const SizedBox(height: 14),
              const Divider(height: 1, color: AppTheme.borderLight),
              const SizedBox(height: 10),
              const Text(
                "Official Verified Sources:",
                style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: AppTheme.textMuted),
              ),
              const SizedBox(height: 6),
              ...message.citations.map(
                (c) => InkWell(
                  onTap: () async {
                    final uri = Uri.parse(c.url);
                    if (await canLaunchUrl(uri)) {
                      await launchUrl(uri, mode: LaunchMode.externalApplication);
                    }
                  },
                  child: Padding(
                    padding: const EdgeInsets.symmetric(vertical: 3),
                    child: Row(
                      children: [
                        const Icon(Icons.link, size: 12, color: AppTheme.maroonPrimary),
                        const SizedBox(width: 6),
                        Expanded(
                          child: Text(
                            "${c.title} ↗",
                            style: const TextStyle(
                              fontSize: 12,
                              color: AppTheme.maroonPrimary,
                              decoration: TextDecoration.underline,
                            ),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ]
          ],
        ),
      ),
    );
  }
}

