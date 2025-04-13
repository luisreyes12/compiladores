package com.mycompany.tp1compiladores;

/**
 * @author Luis Reyes
 */
import javax.swing.*;
import java.io.*;
import java.util.regex.*;
import java.util.*;

public class Tp1Compiladores {

    private static final Map<String, String> TOKEN_PATTERNS = new LinkedHashMap<>();

    static {
        TOKEN_PATTERNS.put("L_LLAVE", "\\{");
        TOKEN_PATTERNS.put("R_LLAVE", "\\}");
        TOKEN_PATTERNS.put("L_CORCHETE", "\\[");
        TOKEN_PATTERNS.put("R_CORCHETE", "\\]");
        TOKEN_PATTERNS.put("COMA", ",");
        TOKEN_PATTERNS.put("DOS_PUNTOS", ":");
        TOKEN_PATTERNS.put("STRING", "\"([^\"\\\\]*(\\\\.[^\"\\\\]*)*)\"");
        TOKEN_PATTERNS.put("NUMBER", "-?\\d+(\\.\\d+)?([eE][+-]?\\d+)?");
        TOKEN_PATTERNS.put("PR_TRUE", "true");
        TOKEN_PATTERNS.put("PR_FALSE", "false");
        TOKEN_PATTERNS.put("PR_NULL", "null");
    }

    private static final Pattern TOKEN_REGEX = Pattern.compile(
            TOKEN_PATTERNS.values().stream().reduce((a, b) -> a + "|" + b).get()
    );

    public static void main(String[] args) {
        // Cuadro de diálogo para seleccionar un archivo JSON
        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setDialogTitle("Selecciona el archivo JSON");
        int userSelection = fileChooser.showOpenDialog(null);

        if (userSelection != JFileChooser.APPROVE_OPTION) {
            JOptionPane.showMessageDialog(null, "No se seleccionó ningún archivo.", "Advertencia", JOptionPane.WARNING_MESSAGE);
            return;
        }

        File selectedFile = fileChooser.getSelectedFile();
        JOptionPane.showMessageDialog(null, "Archivo seleccionado:\n" + selectedFile.getAbsolutePath(), "Archivo Cargado", JOptionPane.INFORMATION_MESSAGE);

        // Pedir ubicación para guardar output.txt
        JFileChooser saveChooser = new JFileChooser();
        saveChooser.setDialogTitle("Elige dónde guardar output.txt");
        saveChooser.setSelectedFile(new File("output.txt"));

        int saveSelection = saveChooser.showSaveDialog(null);
        if (saveSelection != JFileChooser.APPROVE_OPTION) {
            JOptionPane.showMessageDialog(null, "No se seleccionó una ubicación para guardar.", "Advertencia", JOptionPane.WARNING_MESSAGE);
            return;
        }

        File outputFile = saveChooser.getSelectedFile();
        JOptionPane.showMessageDialog(null, "Archivo de salida:\n" + outputFile.getAbsolutePath(), "Ubicación Guardada", JOptionPane.INFORMATION_MESSAGE);

        try {
            BufferedReader reader = new BufferedReader(new FileReader(selectedFile));
            BufferedWriter writer = new BufferedWriter(new FileWriter(outputFile));

            String line;
            while ((line = reader.readLine()) != null) {
                String formattedLine = tokenizeWithSpaces(line);
                writer.write(formattedLine + "\n");
            }

            reader.close();
            writer.close();
            //JOptionPane.showMessageDialog(null, "Análisis léxico completado.\nArchivo guardado en:\n" + outputFile.getAbsolutePath(), "Proceso Completado", JOptionPane.INFORMATION_MESSAGE);

        } catch (IOException e) {
            JOptionPane.showMessageDialog(null, "Error al procesar el archivo:\n" + e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    // Método para tokenizar y mantener los espacios
    public static String tokenizeWithSpaces(String input) {
        StringBuilder formattedLine = new StringBuilder();
        Matcher matcher = TOKEN_REGEX.matcher(input);
        int lastEnd = 0;

        while (matcher.find()) {
            // Mantener el texto antes del token encontrado (esto incluye espacios y tabulaciones)
            formattedLine.append(input, lastEnd, matcher.start());

            // Identificar qué token es y agregarlo
            for (Map.Entry<String, String> entry : TOKEN_PATTERNS.entrySet()) {
                if (matcher.group().matches(entry.getValue())) {
                    formattedLine.append(entry.getKey()).append(" ");
                    break;
                }
            }
            lastEnd = matcher.end();
        }

        // Agregar el resto del texto (en caso de que haya algo después del último token)
        formattedLine.append(input.substring(lastEnd));

        // Asegurarse de que los espacios se mantengan
        return formattedLine.toString();
    }
}
