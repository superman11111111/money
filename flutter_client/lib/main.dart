import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_client/alert.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(MyApp());
}

Future<List<ETFAlerts>> fetchAlerts() async {
  final response = await http.get(Uri.http('62.171.165.127:4000', 'alerts'));
  if (response.statusCode == 200) {
    List e = new List();
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

class _MyHomePageState extends State<MyHomePage> {
  void _incrementCounter() {}
  Future<List<ETFAlerts>> futureAlerts;
  @override
  void initState() {
    super.initState();
    futureAlerts = fetchAlerts();
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
              itemBuilder: (context, i) {
                return ListTile(
                  title: Text(snapshot.data[i].name),
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
