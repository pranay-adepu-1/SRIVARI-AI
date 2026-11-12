class Citation {
  final String title;
  final String url;
  final String source;

  Citation({
    required this.title,
    required this.url,
    required this.source,
  });

  factory Citation.fromJson(Map<String, dynamic> json) {
    return Citation(
      title: json['title'] ?? '',
      url: json['url'] ?? '',
      source: json['source'] ?? 'ttdevasthanams.ap.gov.in',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'title': title,
      'url': url,
      'source': source,
    };
  }
}

class ChatMessageItem {
  final String id;
  final String sender; // 'user' or 'assistant'
  final String content;
  final String language;
  final List<Citation> citations;
  final bool isVoice;
  final DateTime createdAt;

  ChatMessageItem({
    required this.id,
    required this.sender,
    required this.content,
    required this.language,
    this.citations = const [],
    this.isVoice = false,
    required this.createdAt,
  });

  bool get isUser => sender == 'user';

  factory ChatMessageItem.fromJson(Map<String, dynamic> json) {
    var rawCitations = json['citations'] as List? ?? [];
    List<Citation> parsedCitations = rawCitations.map((c) => Citation.fromJson(c)).toList();

    return ChatMessageItem(
      id: json['id'] ?? UniqueKey().toString(),
      sender: json['sender'] ?? 'assistant',
      content: json['content'] ?? '',
      language: json['language'] ?? 'te',
      citations: parsedCitations,
      isVoice: json['is_voice'] ?? false,
      createdAt: DateTime.tryParse(json['created_at'] ?? '') ?? DateTime.now(),
    );
  }
}

class UniqueKey {
  @override
  String toString() => DateTime.now().millisecondsSinceEpoch.toString();
}

