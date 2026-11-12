import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppTheme {
  // Sacred Devotional Color Palette
  static const Color maroonDeep = Color(0xFF5B0000);
  static const Color maroonPrimary = Color(0xFF800000);
  static const Color maroonLight = Color(0xFF991B1B);
  
  static const Color goldPrimary = Color(0xFFD4AF37);
  static const Color goldLight = Color(0xFFF9E79F);
  static const Color goldDark = Color(0xFFAA820A);
  
  static const Color creamBg = Color(0xFFFAF7F2);
  static const Color creamCard = Color(0xFFFFFFFF);
  static const Color saffronAccent = Color(0xFFFF9933);
  
  static const Color textDark = Color(0xFF2A1810);
  static const Color textMuted = Color(0xFF6E6259);
  static const Color borderLight = Color(0xFFEBDDCB);

  // Light Theme
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      primaryColor: maroonPrimary,
      scaffoldBackgroundColor: creamBg,
      colorScheme: const ColorScheme.light(
        primary: maroonPrimary,
        onPrimary: Colors.white,
        secondary: goldPrimary,
        onSecondary: textDark,
        tertiary: saffronAccent,
        surface: creamCard,
        onSurface: textDark,
        error: Color(0xFFBA1A1A),
      ),
      appBarTheme: AppBarTheme(
        backgroundColor: maroonPrimary,
        foregroundColor: Colors.white,
        elevation: 0,
        centerTitle: true,
        titleTextStyle: GoogleFonts.cinzel(
          fontSize: 20,
          fontWeight: FontWeight.bold,
          color: goldLight,
        ),
      ),
      cardTheme: CardTheme(
        color: creamCard,
        elevation: 1.5,
        shadowColor: Colors.black.withOpacity(0.08),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(14),
          side: const BorderSide(color: borderLight, width: 0.8),
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: maroonPrimary,
          foregroundColor: Colors.white,
          elevation: 2,
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(10),
          ),
          textStyle: GoogleFonts.plusJakartaSans(
            fontSize: 15,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),
      textTheme: TextTheme(
        displayLarge: GoogleFonts.cinzel(fontSize: 32, fontWeight: FontWeight.bold, color: maroonPrimary),
        headlineMedium: GoogleFonts.cinzel(fontSize: 22, fontWeight: FontWeight.bold, color: textDark),
        titleLarge: GoogleFonts.plusJakartaSans(fontSize: 18, fontWeight: FontWeight.bold, color: textDark),
        bodyLarge: GoogleFonts.plusJakartaSans(fontSize: 15, color: textDark),
        bodyMedium: GoogleFonts.plusJakartaSans(fontSize: 13, color: textMuted),
      ),
    );
  }

  // Dark Devotional Theme
  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      primaryColor: maroonLight,
      scaffoldBackgroundColor: const Color(0xFF19110E),
      colorScheme: const ColorScheme.dark(
        primary: goldPrimary,
        onPrimary: textDark,
        secondary: saffronAccent,
        surface: Color(0xFF241A16),
        onSurface: Color(0xFFEDE4DC),
        error: Color(0xFFFFB4AB),
      ),
      appBarTheme: AppBarTheme(
        backgroundColor: const Color(0xFF241A16),
        foregroundColor: goldLight,
        elevation: 0,
        centerTitle: true,
        titleTextStyle: GoogleFonts.cinzel(
          fontSize: 20,
          fontWeight: FontWeight.bold,
          color: goldLight,
        ),
      ),
      cardTheme: CardTheme(
        color: const Color(0xFF2A1E19),
        elevation: 2,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(14),
          side: BorderSide(color: goldDark.withOpacity(0.3), width: 0.8),
        ),
      ),
    );
  }
}

