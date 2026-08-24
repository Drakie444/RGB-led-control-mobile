import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:flutter_colorpicker/flutter_colorpicker.dart';
import 'esp_service.dart';


class LedControls extends StatefulWidget {
  const LedControls({super.key});

  @override
  State<LedControls> createState() => _LedControlsState();

}

class _LedControlsState extends State<LedControls> {
  final espService = EspService(dotenv.env['ESP_IP']!);
  Color pickerColor = Colors.red;

  void _updateEsp(Color color){
    int r = (color.r * 255).round();
    int g = (color.g * 255).round();
    int b = (color.b * 255).round();

    espService.sendRgb(r, g, b);
  }

  @override
  Widget build(BuildContext context){
    return Scaffold(
      appBar: AppBar(title: const Text('LED Controls')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            HueRingPicker(pickerColor: pickerColor, onColorChanged: (Color color) {
              setState(() => pickerColor = color);
            },
            enableAlpha: false,
            displayThumbColor: true,
            ),
            const SizedBox(height: 30),
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: pickerColor,
                padding: const EdgeInsets.symmetric(horizontal: 50, vertical: 10)
              ),
              onPressed: () => _updateEsp(pickerColor),
              child: const Text(
                "Set color",
                style: TextStyle(color: Colors.white, fontSize: 18),
              ), 
            ),
          ],
        )
      ),
    );
  }
}