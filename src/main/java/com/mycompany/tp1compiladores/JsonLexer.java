
package com.mycompany.tp1compiladores;
import java.io.*;
import java.util.regex.*;

/**
 *
 * @author Luis Reyes
 */
public class JsonLexer {
    private static final Pattern TOKEN_PATTERN = Pattern.compile(
        "(?<L_LLAVE>\{)|(?<R_LLAVE>\})|(?<L_CORCHETE>\[)|(?<R_CORCHETE>\])|"
        + "(?<COMA>,)|(?<DOS_PUNTOS>:)|"
        + "(?<LITERAL_CADENA>\".*?\")|"
        + "(?<LITERAL_NUM>[0-9]+(\\.[0-9]+)?([eE][+-]?[0-9]+)?)|"
        + "(?<PR_TRUE>true|TRUE)|(?<PR_FALSE>false|FALSE)|(?<PR_NULL>null|NULL)"
    );

    public static void analizarArchivo(String archivoEntrada, String archivoSalida) {
        try (BufferedReader br = new BufferedReader(new FileReader(archivoEntrada));
             BufferedWriter bw = new BufferedWriter(new FileWriter(archivoSalida))) {
            
            String linea;
            while ((linea = br.readLine()) != null) {
                Matcher matcher = TOKEN_PATTERN.matcher(linea);
                StringBuilder resultado = new StringBuilder();
                
                while (matcher.find()) {
                    for (String token : new String[]{"L_LLAVE", "R_LLAVE", "L_CORCHETE", "R_CORCHETE", "COMA", "DOS_PUNTOS", "LITERAL_CADENA", "LITERAL_NUM", "PR_TRUE", "PR_FALSE", "PR_NULL"}) {
                        if (matcher.group(token) != null) {
                            resultado.append(token).append(" ");
                            break;
                        }
                    }
                }
                
                if (resultado.length() > 0) {
                    bw.write(resultado.toString().trim());
                    bw.newLine();
                }
            }
        } catch (IOException e) {
            System.err.println("Error al leer/escribir archivos: " + e.getMessage());
        }
    }
    
    public static void main(String[] args) {
        String archivoEntrada = "entrada.json";
        String archivoSalida = "salida.txt";
        analizarArchivo(archivoEntrada, archivoSalida);
        System.out.println("Análisis léxico completado. Revisa " + archivoSalida);
    }
}

