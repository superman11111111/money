class Alert {
  final String date;
  final int diff2mv;
  final String tk;

  Alert({this.date, this.diff2mv, this.tk});

  factory Alert.fromJson(Map<String, dynamic> json) {
    return Alert(
      date: json['date'],
      diff2mv: json['diff2mv'],
      tk: json['tk'],
    );
  }
}

class ETFAlerts {
  final String name;
  final List<Alert> alerts;

  ETFAlerts({this.name, this.alerts});

  factory ETFAlerts.fromJson(Map<String, dynamic> json) {
    return ETFAlerts(alerts: json['alerts'], name: json['name']);
  }
}
