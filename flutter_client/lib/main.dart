import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_client/alert.dart';
import 'package:http/http.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'alert.dart';

void main() {
  runApp(MyApp());
}

Future<List<ETFAlerts>> fetchAlerts() async {
  final response = await get('http://62.171.165.127:4000/alerts?d=3');
  if (response.statusCode == 200) {
    List<ETFAlerts> e = new List();
    for (var jj in jsonDecode(response.body)) {
      e.add(ETFAlerts.fromJson(jj));
    }
    // for (var jj in jsonDecode(response.body)) {
    //   print(jj);
    //   e.add(ETFAlerts.fromJson(jj));
    // }
    // print(e);
    return e;
  } else {
    throw Exception('Failed');
  }
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class SecondScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold();
  }
}

class _MyHomePageState extends State<MyHomePage> {
  void _incrementCounter() {
    // newNotf("Increment", "this bitch");
  }

  Future<List<ETFAlerts>> futureAlerts;
  FlutterLocalNotificationsPlugin flutterLocalNotificationsPlugin;
  @override
  void initState() {
    super.initState();
    // initNotf();
    futureAlerts = fetchAlerts();
  }

  void initNotf() async {
    flutterLocalNotificationsPlugin = FlutterLocalNotificationsPlugin();
    const AndroidInitializationSettings initializationSettingsAndroid =
        AndroidInitializationSettings('app_icon');
    final IOSInitializationSettings initializationSettingsIOS =
        IOSInitializationSettings(
            onDidReceiveLocalNotification: onDidReceiveLocalNotification);
    final MacOSInitializationSettings initializationSettingsMacOS =
        MacOSInitializationSettings();
    final InitializationSettings initializationSettings =
        InitializationSettings(
            android: initializationSettingsAndroid,
            iOS: initializationSettingsIOS,
            macOS: initializationSettingsMacOS);
    await flutterLocalNotificationsPlugin.initialize(initializationSettings,
        onSelectNotification: selectNotification);
  }

  void newNotf(String title, String body) async {
    const AndroidNotificationDetails androidPlatformChannelSpecifics =
        AndroidNotificationDetails('1', 'Test123', 'Test123',
            importance: Importance.max,
            priority: Priority.high,
            showWhen: false);
    const NotificationDetails platformChannelSpecifics =
        NotificationDetails(android: androidPlatformChannelSpecifics);
    await flutterLocalNotificationsPlugin
        .show(0, title, body, platformChannelSpecifics, payload: 'item x');
  }

  Future selectNotification(String payload) async {
    if (payload != null) {
      debugPrint('notification payload: $payload');
    }
    await Navigator.push(
      context,
      MaterialPageRoute<void>(builder: (context) => SecondScreen()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Center(
          child: FutureBuilder<List<ETFAlerts>>(
        future: futureAlerts,
        builder: (context, snapshot) {
          if (snapshot.hasData) {
            return ListView.builder(
              itemCount: snapshot.data.length,
              itemBuilder: (context, i) {
                return ListTile(
                  leading: GestureDetector(
                    behavior: HitTestBehavior.translucent,
                    onTap: () {},
                    child: Container(
                      alignment: Alignment.center,
                      width: 48,
                      height: 48,
                      padding: EdgeInsets.symmetric(vertical: 4.0),
                      child: Text(snapshot.data[i].alerts.length.toString()),
                    ),
                  ),
                  title: Text(snapshot.data[i].name),
                  onTap: () {
                    Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) =>
                              AlertsScreen(etfAlerts: snapshot.data[i]),
                        ));
                  },
                );
              },
            );
          } else if (snapshot.hasError) {
            return Text('${snapshot.error}');
          }
          return CircularProgressIndicator();
        },
      )),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementCounter,
        tooltip: 'Increment',
        child: Icon(Icons.add),
      ),
    );
  }
}

class AlertsScreen extends StatelessWidget {
  final ETFAlerts etfAlerts;

  const AlertsScreen({Key key, this.etfAlerts}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return Scaffold(
      appBar: AppBar(
        title: Text(etfAlerts.name),
        actions: <Widget>[
          FlatButton(
            textColor: Colors.white,
            onPressed: () {
              // setState(() {
              etfAlerts.alerts.sort((a, b) => a.diff2mv.compareTo(b.diff2mv));
              // });
            },
            child: Text("Sort"),
            shape: CircleBorder(side: BorderSide(color: Colors.transparent)),
          ),
        ],
      ),
      body: Center(
        child: ListView.builder(
          itemCount: etfAlerts.alerts.length,
          itemBuilder: (context, i) {
            return ListTile(
              title: Text(etfAlerts.alerts[i].tk),
              leading: Text(etfAlerts.alerts[i].date),
              subtitle: Text(etfAlerts.alerts[i].diff2mv.toString()),
            );
          },
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Navigator.pop(context);
        },
        tooltip: "Go back",
      ),
    );
  }
}

Future onDidReceiveLocalNotification(
    int id, String title, String body, String payload) {}
