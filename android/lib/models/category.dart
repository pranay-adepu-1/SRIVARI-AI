class AnnouncementCategoryItem {
  final String id;
  final String nameEn;
  final String nameTe;
  final String slug;
  final String iconName;
  final String colorHex;
  final int displayOrder;

  AnnouncementCategoryItem({
    required this.id,
    required this.nameEn,
    required this.nameTe,
    required this.slug,
    required this.iconName,
    required this.colorHex,
    required this.displayOrder,
  });

  String getName(String lang) => lang == 'te' ? nameTe : nameEn;

  factory AnnouncementCategoryItem.fromJson(Map<String, dynamic> json) {
    return AnnouncementCategoryItem(
      id: json['id'] ?? '',
      nameEn: json['name_en'] ?? '',
      nameTe: json['name_te'] ?? '',
      slug: json['slug'] ?? '',
      iconName: json['icon_name'] ?? 'notifications',
      colorHex: json['color_hex'] ?? '#D4AF37',
      displayOrder: json['display_order'] ?? 0,
    );
  }
}

