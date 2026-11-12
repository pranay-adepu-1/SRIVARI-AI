class AccommodationGuideItem {
  final String categoryEn;
  final String categoryTe;
  final String location;
  final String tariffRange;
  final String cautionDeposit;
  final int maxStayHours;
  final List<String> guidelinesEn;
  final List<String> guidelinesTe;
  final String officialLink;

  AccommodationGuideItem({
    required this.categoryEn,
    required this.categoryTe,
    required this.location,
    required this.tariffRange,
    required this.cautionDeposit,
    required this.maxStayHours,
    required this.guidelinesEn,
    required this.guidelinesTe,
    required this.officialLink,
  });

  String getCategory(String lang) => lang == 'te' ? categoryTe : categoryEn;
  List<String> getGuidelines(String lang) => lang == 'te' ? guidelinesTe : guidelinesEn;

  factory AccommodationGuideItem.fromJson(Map<String, dynamic> json) {
    return AccommodationGuideItem(
      categoryEn: json['category_en'] ?? '',
      categoryTe: json['category_te'] ?? '',
      location: json['location'] ?? '',
      tariffRange: json['tariff_range'] ?? '',
      cautionDeposit: json['caution_deposit'] ?? '',
      maxStayHours: json['max_stay_hours'] ?? 24,
      guidelinesEn: List<String>.from(json['guidelines_en'] ?? []),
      guidelinesTe: List<String>.from(json['guidelines_te'] ?? []),
      officialLink: json['official_link'] ?? 'https://ttdevasthanams.ap.gov.in/',
    );
  }
}

