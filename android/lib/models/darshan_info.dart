class DarshanGuideItem {
  final String id;
  final String nameEn;
  final String nameTe;
  final String cost;
  final String bookingMode;
  final String reportingLocationEn;
  final String reportingLocationTe;
  final String descriptionEn;
  final String descriptionTe;
  final List<String> guidelinesEn;
  final List<String> guidelinesTe;
  final String officialLink;

  DarshanGuideItem({
    required this.id,
    required this.nameEn,
    required this.nameTe,
    required this.cost,
    required this.bookingMode,
    required this.reportingLocationEn,
    required this.reportingLocationTe,
    required this.descriptionEn,
    required this.descriptionTe,
    required this.guidelinesEn,
    required this.guidelinesTe,
    required this.officialLink,
  });

  String getName(String lang) => lang == 'te' ? nameTe : nameEn;
  String getDescription(String lang) => lang == 'te' ? descriptionTe : descriptionEn;
  String getReportingLocation(String lang) => lang == 'te' ? reportingLocationTe : reportingLocationEn;
  List<String> getGuidelines(String lang) => lang == 'te' ? guidelinesTe : guidelinesEn;

  factory DarshanGuideItem.fromJson(Map<String, dynamic> json) {
    return DarshanGuideItem(
      id: json['id'] ?? '',
      nameEn: json['name_en'] ?? '',
      nameTe: json['name_te'] ?? '',
      cost: json['cost'] ?? '',
      bookingMode: json['booking_mode'] ?? '',
      reportingLocationEn: json['reporting_location_en'] ?? '',
      reportingLocationTe: json['reporting_location_te'] ?? '',
      descriptionEn: json['description_en'] ?? '',
      descriptionTe: json['description_te'] ?? '',
      guidelinesEn: List<String>.from(json['guidelines_en'] ?? []),
      guidelinesTe: List<String>.from(json['guidelines_te'] ?? []),
      officialLink: json['official_link'] ?? 'https://ttdevasthanams.ap.gov.in/',
    );
  }
}

