import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_client/alert.dart';
import 'package:http/http.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'alert.dart';

void main() {
  runApp(MyApp());
}

Future<List<ETFAlerts>> fetchAlerts(int days) async {
  final response = await get('http://62.171.165.127:4000/alerts?d=$days');
  if (response.statusCode == 200) {
    List<ETFAlerts> e = new List();
    for (var jj in jsonDecode(response.body)) {
      e.add(ETFAlerts.fromJson(jj));
    }
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
  int days = 1;

  Future<List<ETFAlerts>> futureAlerts;
  FlutterLocalNotificationsPlugin flutterLocalNotificationsPlugin;
  @override
  void initState() {
    controller = new TextEditingController();
    super.initState();
    futureAlerts = fetchAlerts(days);
  }

  TextEditingController controller;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
          title: Text(widget.title),
          actions: [
            IconButton(
              icon: Icon(Icons.settings),
              onPressed: () {
                showDialog(
                    child: new Dialog(
                      child: new Column(
                        children: <Widget>[
                          new TextField(
                            keyboardType: TextInputType.number,
                            decoration:
                                new InputDecoration(hintText: "Update Info"),
                            controller: controller,
                          ),
                          new FlatButton(
                            child: new Text("Save"),
                            onPressed: () {
                              setState(() {
                                days = int.parse(controller.text);
                                futureAlerts = fetchAlerts(days);
                                // this._text = _c.text;
                              });
                              Navigator.pop(context);
                            },
                          )
                        ],
                      ),
                    ),
                    context: context);
              },
            ),
          ],
          leading: Center(
            child: Text(
              days.toString(),
              style: TextStyle(fontSize: 20.0),
            ),
          )),
      body: Center(
        child: FutureBuilder<List<ETFAlerts>>(
          future: futureAlerts,
          builder: (context, snapshot) {
            if (snapshot.hasData) {
              return ListView.builder(
                itemCount: snapshot.data.length,
                itemBuilder: (context, i) {
                  return ListTile(
                    leading: Text(snapshot.data[i].alerts.length.toString()),
                    title: Text(snapshot.data[i].name),
                    onTap: () {
                      showDialog(
                        context: context,
                        child: new Dialog(
                          child: new Center(
                            child: ListView.builder(
                              itemCount: snapshot.data[i].alerts.length,
                              itemBuilder: (context, j) {
                                return ListTile(
                                  title: Text(snapshot.data[i].alerts[j].tk),
                                  leading:
                                      Text(snapshot.data[i].alerts[j].date),
                                  subtitle: Text(snapshot
                                      .data[i].alerts[j].diff2mv
                                      .toString()),
                                );
                              },
                            ),
                          ),
                        ),
                      );
                    },
                  );
                },
              );
            } else if (snapshot.hasError) {
              return Text('${snapshot.error}');
            }
            return CircularProgressIndicator();
          },
        ),
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
