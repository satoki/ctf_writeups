/*
 * Decompiled with CFR 0.152.
 * 
 * Could not load the following classes:
 *  javax.servlet.Servlet
 *  javax.servlet.ServletOutputStream
 *  javax.servlet.annotation.MultipartConfig
 *  javax.servlet.http.HttpServlet
 *  javax.servlet.http.HttpServletRequest
 *  javax.servlet.http.HttpServletResponse
 *  javax.servlet.http.Part
 *  org.eclipse.jetty.server.Handler
 *  org.eclipse.jetty.server.Server
 *  org.eclipse.jetty.servlet.ServletContextHandler
 *  org.eclipse.jetty.servlet.ServletHolder
 */
package ctf.jargon;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.ObjectInputStream;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;
import javax.servlet.Servlet;
import javax.servlet.ServletOutputStream;
import javax.servlet.annotation.MultipartConfig;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.Part;
import org.eclipse.jetty.server.Handler;
import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.servlet.ServletContextHandler;
import org.eclipse.jetty.servlet.ServletHolder;

@MultipartConfig
public class App
extends HttpServlet {
    private static Connection conn;

    private void ensureDB() {
        try {
            File dir;
            if (conn == null || conn.isClosed()) {
                conn = DriverManager.getConnection("jdbc:sqlite:/app/jargon.db");
                Statement st = conn.createStatement();
                st.execute("CREATE TABLE IF NOT EXISTS tickets (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, message TEXT)");
                ResultSet rs = st.executeQuery("SELECT COUNT(*) as c FROM tickets");
                if (rs.next() && rs.getInt("c") == 0) {
                    for (int i = 1; i <= 50; ++i) {
                        String name = "admin";
                        String msg = i == 30 ? "Internal note: Compiled jar is stored in /app/target/jargon.jar" : (i % 10 == 0 ? "DEBUG LOG: NullPointerException at ctf.jargon.App.doPost(App.java:132)" : (i % 13 == 0 ? "Reminder: db creds are admin:password123 (change before prod!)" : (i % 17 == 0 ? "API_KEY=sk_test_51JargonSuperLeaky" + i : (i % 7 == 0 ? "SQL dump fragment: INSERT INTO users VALUES(1,'root','toor');" : "Hello from seeded admin ticket #" + i))));
                        try (PreparedStatement ps = conn.prepareStatement("INSERT INTO tickets (id, name, message) VALUES (?, ?, ?)");){
                            ps.setInt(1, i);
                            ps.setString(2, name);
                            ps.setString(3, msg);
                            ps.executeUpdate();
                            continue;
                        }
                    }
                }
            }
            if (!(dir = new File("/app/uploads")).exists()) {
                dir.mkdirs();
            }
            for (int i = 1; i <= 50; ++i) {
                File f = new File(dir, "ticket-" + i + ".txt");
                if (f.exists()) continue;
                try (FileWriter fw = new FileWriter(f);){
                    fw.write("Ticket #" + i + "\nSeeded file for ticket.\n");
                    continue;
                }
            }
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }

    private String header(String title) {
        return "<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>" + title + " - Jargon Corp</title><script src='https://cdn.tailwindcss.com'></script></head><body class='bg-gray-900 text-gray-100 font-sans'><nav class='bg-gray-800 shadow mb-8'><div class='max-w-6xl mx-auto px-4 py-4 flex justify-between'><a href='/' class='text-indigo-400 text-xl font-bold'>Jargon Corp</a><div class='space-x-6'><a href='/' class='hover:text-indigo-300'>Home</a><a href='/tickets?user=admin' class='hover:text-indigo-300'>Tickets</a></div></div></nav><div class='max-w-4xl mx-auto px-4'>";
    }

    private String footer() {
        return "</div><footer class='mt-12 bg-gray-800 py-4 text-center text-gray-400 text-sm'>\u00a9 2025 Jargon Corp \u2014 All rights reserved.</footer></body></html>";
    }

    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        this.ensureDB();
        resp.setContentType("text/html");
        resp.getWriter().println(this.header("Home") + "<h1 class='text-4xl font-bold text-indigo-400 mb-6 text-center'>Welcome to Jargon Corp</h1><p class='text-center text-lg mb-12'>Trusted Solutions for Modern Businesses</p><div class='bg-gray-800 shadow-lg rounded-lg p-8'>  <h2 class='text-2xl font-semibold mb-4 text-indigo-300'>Contact Us</h2>  <form method='POST' action='/contact' enctype='multipart/form-data' class='space-y-4'>    <div><label class='block mb-1 text-sm font-medium'>Name</label>      <input type='text' name='name' class='w-full border rounded p-2 bg-gray-700 text-white'></div>    <div><label class='block mb-1 text-sm font-medium'>Message</label>      <textarea name='message' class='w-full border rounded p-2 bg-gray-700 text-white'></textarea></div>    <div><label class='block mb-1 text-sm font-medium'>Attachment</label>      <input type='file' name='file' class='w-full text-gray-200'></div>    <button type='submit' class='bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700'>Send</button>  </form></div>" + this.footer());
    }

    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String ctype = req.getContentType();
        resp.setContentType("text/html");
        if (ctype != null && ctype.startsWith("application/octet-stream")) {
            try (ObjectInputStream ois = new ObjectInputStream((InputStream)req.getInputStream());){
                Object obj = ois.readObject();
                resp.getWriter().println(this.header("Exploit") + "<div class='bg-red-900 p-6 rounded'><h2 class='text-xl font-bold text-red-300 mb-2'>[!] Deserialization Result</h2><p class='text-gray-200'>" + obj.toString() + "</p></div>" + this.footer());
            }
            catch (Exception e) {
                resp.getWriter().println(this.header("Error") + "<p class='text-red-400'>Error: " + e.getMessage() + "</p>" + this.footer());
            }
        } else {
            int ticketId;
            String name;
            block58: {
                this.ensureDB();
                name = req.getParameter("name");
                String message = req.getParameter("message");
                ticketId = -1;
                try (PreparedStatement ps = conn.prepareStatement("INSERT INTO tickets (name, message) VALUES (?, ?)", 1);){
                    Part filePart;
                    ps.setString(1, name);
                    ps.setString(2, message);
                    ps.executeUpdate();
                    ResultSet keys = ps.getGeneratedKeys();
                    if (keys.next()) {
                        ticketId = keys.getInt(1);
                    }
                    if ((filePart = req.getPart("file")) == null || filePart.getSize() <= 0L) break block58;
                    File dir = new File("/app/uploads");
                    if (!dir.exists()) {
                        dir.mkdirs();
                    }
                    try (InputStream is = filePart.getInputStream();
                         FileOutputStream fos = new FileOutputStream(new File(dir, "ticket-" + ticketId + "-" + filePart.getSubmittedFileName()));){
                        int len;
                        byte[] buf = new byte[4096];
                        while ((len = is.read(buf)) > 0) {
                            fos.write(buf, 0, len);
                        }
                    }
                }
                catch (Exception e) {
                    e.printStackTrace();
                }
            }
            resp.getWriter().println(this.header("Submitted") + "<div class='bg-green-900 p-6 rounded'><h2 class='text-2xl font-bold text-green-300 mb-2'>Thanks " + this.escape(name) + "!</h2><p>We received your message.</p><p>Your ticket number is <span class='font-mono text-indigo-400'>" + ticketId + "</span></p><a href='/ticket?id=" + ticketId + "' class='mt-4 inline-block text-indigo-400 underline'>View Ticket</a></div>" + this.footer());
        }
    }

    private void showTicket(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String id = req.getParameter("id");
        resp.setContentType("text/html");
        try (Statement st = conn.createStatement();){
            ResultSet rs = st.executeQuery("SELECT * FROM tickets WHERE id=" + id);
            if (rs.next()) {
                resp.getWriter().println(this.header("Ticket #" + id) + "<div class='bg-gray-800 p-6 rounded'><h2 class='text-2xl font-bold text-indigo-400 mb-4'>Ticket #" + rs.getInt("id") + "</h2><p><span class='font-semibold'>From:</span> " + rs.getString("name") + "</p><p class='mt-2 text-gray-200'>" + rs.getString("message") + "</p><a href='/download?id=" + rs.getInt("id") + "' class='mt-4 inline-block bg-indigo-600 px-4 py-2 rounded hover:bg-indigo-700'>Download Attachment</a></div>" + this.footer());
            } else {
                resp.getWriter().println(this.header("Ticket Not Found") + "<p>No such ticket.</p>" + this.footer());
            }
        }
        catch (Exception e) {
            resp.getWriter().println(this.header("Error") + "<p>Error: " + e.getMessage() + "</p>" + this.footer());
        }
    }

    private void listTickets(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String user = req.getParameter("user");
        resp.setContentType("text/html");
        try (Statement st = conn.createStatement();){
            ResultSet rs = st.executeQuery("SELECT * FROM tickets WHERE name='" + user + "'");
            resp.getWriter().println(this.header("Tickets for " + user) + "<h2 class='text-3xl font-bold text-indigo-400 mb-6'>Tickets for " + user + "</h2><div class='grid grid-cols-1 gap-6'>");
            while (rs.next()) {
                resp.getWriter().println("<div class='bg-gray-800 p-6 rounded shadow'><a class='text-xl font-semibold text-indigo-300 underline' href='/ticket?id=" + rs.getInt("id") + "'>Ticket #" + rs.getInt("id") + "</a><p class='mt-2 text-gray-300'>" + rs.getString("message") + "</p></div>");
            }
            resp.getWriter().println("</div>" + this.footer());
        }
        catch (Exception e) {
            resp.getWriter().println(this.header("Error") + "<p>Error: " + e.getMessage() + "</p>" + this.footer());
        }
    }

    private void downloadFile(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        block26: {
            String fileParam = req.getParameter("id");
            File f = new File(fileParam);
            if (f.exists() && f.isFile()) {
                resp.setContentType("application/octet-stream");
                resp.setHeader("Content-Disposition", "attachment; filename=\"" + f.getName() + "\"");
                try (FileInputStream fis = new FileInputStream(f);
                     ServletOutputStream os = resp.getOutputStream();){
                    int len;
                    byte[] buf = new byte[4096];
                    while ((len = fis.read(buf)) > 0) {
                        os.write(buf, 0, len);
                    }
                    break block26;
                }
            }
            resp.getWriter().println(this.header("Error") + "<p>File not found</p>" + this.footer());
        }
    }

    private String escape(String s) {
        if (s == null) {
            return "";
        }
        return s.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
    }

    public static void main(String[] args) throws Exception {
        Class.forName("org.sqlite.JDBC");
        Server server = new Server(8080);
        ServletContextHandler context = new ServletContextHandler(1);
        context.setContextPath("/");
        server.setHandler((Handler)context);
        context.addServlet(new ServletHolder((Servlet)new App()), "/");
        context.addServlet(new ServletHolder((Servlet)new App()), "/contact");
        context.addServlet(new ServletHolder((Servlet)new HttpServlet(){

            protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
                new App().showTicket(req, resp);
            }
        }), "/ticket");
        context.addServlet(new ServletHolder((Servlet)new HttpServlet(){

            protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
                new App().listTickets(req, resp);
            }
        }), "/tickets");
        context.addServlet(new ServletHolder((Servlet)new HttpServlet(){

            protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
                new App().downloadFile(req, resp);
            }
        }), "/download");
        server.start();
        server.join();
    }
}
