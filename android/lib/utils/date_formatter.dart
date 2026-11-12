import 'package:intl/intl.dart';

class DateFormatter {
  static String formatDevotionalDate(DateTime dateTime, String lang) {
    if (lang == 'te') {
      final formatter = DateFormat('dd MMMM yyyy, hh:mm a');
      return formatter.format(dateTime);
    } else {
      final formatter = DateFormat('MMM dd, yyyy • hh:mm a');
      return formatter.format(dateTime);
    }
  }

  static String timeAgo(DateTime dateTime, String lang) {
    final diff = DateTime.now().difference(dateTime);
    if (diff.inMinutes < 60) {
      return lang == 'te' ? "${diff.inMinutes} నిమిషాల క్రితం" : "${diff.inMinutes}m ago";
    } else if (diff.inHours < 24) {
      return lang == 'te' ? "${diff.inHours} గంటల క్రితం" : "${diff.inHours}h ago";
    } else {
      return lang == 'te' ? "${diff.inDays} రోజుల క్రితం" : "${diff.inDays}d ago";
    }
  }
}

