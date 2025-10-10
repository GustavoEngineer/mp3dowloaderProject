import 'package:flutter/material.dart';
import 'package:dio/dio.dart';

// Cambia esta URL por la dirección de tu servidor.
// Para emulador de Android, usa 'http://10.0.2.2:5000'
// Para iOS o dispositivo físico, usa la IP de tu máquina local,
// por ejemplo: 'http://192.168.1.100:5000'
final dio = Dio(BaseOptions(baseUrl: 'http://192.168.137.1:5000'));

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MP3 Downloader',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const DownloadPage(),
    );
  }
}

class DownloadPage extends StatefulWidget {
  const DownloadPage({super.key});

  @override
  State<DownloadPage> createState() => _DownloadPageState();
}

class _DownloadPageState extends State<DownloadPage> {
  final TextEditingController _urlController = TextEditingController();
  bool _isDownloading = false;
  String _message = 'Ingresa una URL de YouTube para descargar';

  Future<void> _downloadMp3() async {
    final url = _urlController.text.trim();
    if (url.isEmpty) {
      setState(() {
        _message = 'Por favor, ingresa una URL.';
      });
      return;
    }

    setState(() {
      _isDownloading = true;
      _message = 'Iniciando descarga...';
    });

    try {
      final response = await dio.post('/descargar-mp3', data: {'url': url});

      if (response.statusCode == 200) {
        setState(() {
          _message = '✅ ¡Descarga completada! ' + response.data['mensaje'];
        });
      } else {
        setState(() {
          _message = '❌ Error: ' + response.data['mensaje'];
        });
      }
    } on DioException catch (e) {
      setState(() {
        _message = '❌ Error de conexión: ${e.message}';
      });
    } finally {
      setState(() {
        _isDownloading = false;
      });
    }
  }

  @override
  void dispose() {
    _urlController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text('MP3 Downloader'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: <Widget>[
            const Text(
              'Descargar audio de YouTube',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 20),
            TextField(
              controller: _urlController,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'URL del video',
                hintText: 'Pega aquí la URL de YouTube...',
              ),
              keyboardType: TextInputType.url,
            ),
            const SizedBox(height: 20),
            ElevatedButton.icon(
              onPressed: _isDownloading ? null : _downloadMp3,
              icon: _isDownloading
                  ? const CircularProgressIndicator(color: Colors.white)
                  : const Icon(Icons.download),
              label: Text(_isDownloading ? 'Descargando...' : 'Descargar MP3'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 15),
              ),
            ),
            const SizedBox(height: 20),
            Text(
              _message,
              style: const TextStyle(fontSize: 16),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}
