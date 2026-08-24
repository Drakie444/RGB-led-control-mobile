import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'esp_service.dart';


class LedControls extends StatefulWidget {
  const LedControls({super.key});

  @override
  State<LedControls> createState() => _LedControlsState();

}

class _LedControlsState extends State<LedControls> {
  final espService = EspService(dotenv.env['ESP_IP']!);

  double r=0, g=0, b=0;
  void _updateEsp(){
    espService.sendRgb(r.toInt(), g.toInt(), b.toInt());
  }

  @override
  Widget build(BuildContext context){
    return Scaffold(
      appBar: AppBar(title: const Text('LED Controls')),
      body: Center(
        child: Slider(
          value: r, 
          min: 0,
          max: 255, 
          onChanged: (val) => setState(() => r = val), 
          onChangeEnd: (_) => _updateEsp(),
        ),
      ),
    );
  }
}