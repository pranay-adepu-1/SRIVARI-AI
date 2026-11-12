import 'package:flutter_test/flutter_test.dart';
import 'package:srivari_ai/models/announcement.dart';
import 'package:srivari_ai/models/chat_message.dart';
import 'package:srivari_ai/utils/date_formatter.dart';
import 'package:srivari_ai/utils/constants.dart';

void main() {
  group('Srivari AI Flutter Unit Tests', () {
    test('Announcement model parses json correctly', () {
      final json = {
        'id': 'test_101',
        'title_en': 'TTD Special Entry Darshan Quota Released',
        'title_te': 'రూ. 300 ప్రత్యేక ప్రవేశ దర్శనం కోటా విడుదల',
        'content_en': 'Book on official portal.',
        'content_te': 'అధికారిక వెబ్‌సైట్ ద్వారా బుక్ చేసుకోండి.',
        'source_url': 'https://news.tirumala.org/sample',
        'source_domain': 'news.tirumala.org',
        'publication_date': '2026-04-01T09:00:00Z',
        'is_verified': true,
        'is_quota_alert': true,
        'is_bookmarked': false,
      };

      final announcement = Announcement.fromJson(json);

      expect(announcement.id, 'test_101');
      expect(announcement.getTitle('en'), 'TTD Special Entry Darshan Quota Released');
      expect(announcement.getTitle('te'), 'రూ. 300 ప్రత్యేక ప్రవేశ దర్శనం కోటా విడుదల');
      expect(announcement.isQuotaAlert, true);
      expect(announcement.isVerified, true);
    });

    test('Chat message and citation model parsing', () {
      final json = {
        'id': 'msg_01',
        'sender': 'assistant',
        'content': 'Om Namo Venkatesaya! Guidelines verified.',
        'language': 'en',
        'citations': [
          {
            'title': 'TTD Booking Portal',
            'url': 'https://ttdevasthanams.ap.gov.in/',
            'source': 'ttdevasthanams.ap.gov.in'
          }
        ],
        'is_voice': false,
        'created_at': '2026-04-01T10:00:00Z',
      };

      final msg = ChatMessageItem.fromJson(json);

      expect(msg.sender, 'assistant');
      expect(msg.isUser, false);
      expect(msg.citations.length, 1);
      expect(msg.citations.first.title, 'TTD Booking Portal');
    });

    test('Devotional DateFormatter timeAgo calculation', () {
      final now = DateTime.now();
      final fiveMinsAgo = now.subtract(const Duration(minutes: 5));

      final teAgo = DateFormatter.timeAgo(fiveMinsAgo, 'te');
      final enAgo = DateFormatter.timeAgo(fiveMinsAgo, 'en');

      expect(teAgo, contains('నిమిషాల క్రితం'));
      expect(enAgo, contains('5m ago'));
    });

    test('Official TTD Portals validation', () {
      expect(AppConstants.ttdBookingPortal, 'https://ttdevasthanams.ap.gov.in/');
      expect(AppConstants.ttdNewsPortal, 'https://news.tirumala.org/');
      expect(AppConstants.ttdMainPortal, 'https://www.tirumala.org/');
    });
  });
}

