import 'package:http/http.dart' as http;

class EspService {
  final String ipAddress;

  EspService(this.ipAddress);

  Future<bool> sendRgb(int r, int  g, int b) async {
    final url = Uri.parse('http://$ipAddress/set?r=$r&g=$g&b=$b');
    try {
       final response = await http.get(url).timeout(const Duration(seconds: 5));
       return response.statusCode == 200;
    } catch (e) {
      print("Error connecting: $e");
      return false;
    }
  }
}