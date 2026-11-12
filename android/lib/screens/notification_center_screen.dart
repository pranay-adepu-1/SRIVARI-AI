import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import '../providers/language_provider.dart';
import '../services/api_service.dart';
import '../models/notification_item.dart';
import '../utils/theme.dart';
import '../utils/date_formatter.dart';

class NotificationCenterScreen extends StatefulWidget {
  const NotificationCenterScreen({super.key});

  @override
  State<NotificationCenterScreen> createState() => _NotificationCenterScreenState();
}

class _NotificationCenterScreenState extends State<NotificationCenterScreen> {
  final ApiService _apiService = ApiService();
  List<NotificationItem> _notifications = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadNotifications();
  }

  Future<void> _loadNotifications() async {
    final list = await _apiService.getNotificationHistory();
    setState(() {
      _notifications = list;
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    final isTe = Provider.of<LanguageProvider>(context).isTelugu;
    final lang = isTe ? 'te' : 'en';

    return Scaffold(
      appBar: AppBar(
        title: Text(
          isTe ? "నోటిఫికేషన్ కేంద్రం" : "Notification Centre",
          style: GoogleFonts.cinzel(fontSize: 16, fontWeight: FontWeight.bold),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              setState(() => _isLoading = true);
              _loadNotifications();
            },
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator(color: AppTheme.maroonPrimary))
          : _notifications.isEmpty
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Icon(Icons.notifications_off_outlined, size: 52, color: AppTheme.textMuted),
                      const SizedBox(height: 12),
                      Text(
                        isTe ? "ఎలాంటి నోటిఫికేషన్లు లేవు" : "No notifications received yet",
                        style: const TextStyle(color: AppTheme.textMuted),
                      ),
                    ],
                  ),
                )
              : ListView.builder(
                  padding: const EdgeInsets.all(16),
                  itemCount: _notifications.length,
                  itemBuilder: (context, index) {
                    final item = _notifications[index];
                    final isQuota = item.notificationType == 'quota_alert';

                    return Container(
                      margin: const EdgeInsets.only(bottom: 12),
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(
                          color: isQuota ? AppTheme.goldPrimary : AppTheme.borderLight,
                          width: isQuota ? 1.2 : 0.8,
                        ),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black.withOpacity(0.03),
                            blurRadius: 4,
                            offset: const Offset(0, 2),
                          ),
                        ],
                      ),
                      child: Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Container(
                            padding: const EdgeInsets.all(8),
                            decoration: BoxDecoration(
                              color: isQuota
                                  ? AppTheme.saffronAccent.withOpacity(0.12)
                                  : AppTheme.maroonPrimary.withOpacity(0.08),
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: Icon(
                              isQuota ? Icons.alarm : Icons.campaign,
                              color: isQuota ? AppTheme.saffronAccent : AppTheme.maroonPrimary,
                              size: 22,
                            ),
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    Expanded(
                                      child: Text(
                                        item.getTitle(lang),
                                        style: GoogleFonts.plusJakartaSans(
                                          fontWeight: FontWeight.bold,
                                          fontSize: 14,
                                          color: AppTheme.textDark,
                                        ),
                                      ),
                                    ),
                                    Text(
                                      DateFormatter.timeAgo(item.sentAt, lang),
                                      style: const TextStyle(fontSize: 10, color: AppTheme.textMuted),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 6),
                                Text(
                                  item.getBody(lang),
                                  style: const TextStyle(fontSize: 13, color: AppTheme.textMuted, height: 1.4),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    );
                  },
                ),
    );
  }
}

