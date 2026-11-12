import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/language_provider.dart';
import '../utils/constants.dart';
import '../utils/theme.dart';

class DisclaimerBanner extends StatelessWidget {
  const DisclaimerBanner({super.key});

  @override
  Widget build(BuildContext context) {
    final isTe = Provider.of<LanguageProvider>(context).isTelugu;

    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: const Color(0xFFFFFBEA),
        border: Border.all(color: AppTheme.goldPrimary.withOpacity(0.5)),
        borderRadius: BorderRadius.circular(10),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Icon(Icons.info_outline, color: AppTheme.goldDark, size: 20),
          const SizedBox(width: 10),
          Expanded(
            child: Text(
              isTe ? AppConstants.disclaimerTe : AppConstants.disclaimerEn,
              style: const TextStyle(
                fontSize: 11,
                color: AppTheme.textDark,
                height: 1.4,
              ),
            ),
          ),
        ],
      ),
    );
  }
}

