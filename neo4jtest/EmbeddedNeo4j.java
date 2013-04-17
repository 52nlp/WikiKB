

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import org.neo4j.graphdb.Direction;
import org.neo4j.graphdb.GraphDatabaseService;
import org.neo4j.graphdb.Node;
import org.neo4j.graphdb.Relationship;
import org.neo4j.graphdb.RelationshipType;
import org.neo4j.graphdb.Transaction;
import org.neo4j.graphdb.factory.GraphDatabaseFactory;
import org.neo4j.graphdb.index.Index;
import org.neo4j.kernel.impl.util.FileUtils;

public class EmbeddedNeo4j
{
    private static final String DB_PATH = "/home/coderz/soft/lda/graph.db";
    private static final String INPUT = "/home/coderz/soft/lda/yagoFacts.clean";
    //private static final String INPUT = "/media/coderz/data/projects/lda/test.db";

    private static Index<Node> nodeIndex;
    private static Index<Relationship> relIndex;
    private static final String NAME_KEY = "name";
    private static final String REK_KEY = "rel";
    String greeting;
    // START SNIPPET: vars
    GraphDatabaseService graphDb;
    Relationship relationship;
    BufferedReader br;
    FileReader fr;
    
	private Node foundNode;
    // END SNIPPET: vars

    // START SNIPPET: createReltype
    private static enum RelTypes implements RelationshipType
    {
        KNOWS
    }
    // END SNIPPET: createReltype

    public static void main( final String[] args ) throws IOException
    {
        EmbeddedNeo4j hello = new EmbeddedNeo4j();
        hello.createDb();
        hello.shutDown();
    }

    void createDb() throws IOException
    {
        clearDb();
        // START SNIPPET: startDb
        graphDb = new GraphDatabaseFactory().newEmbeddedDatabase( DB_PATH );
        nodeIndex = graphDb.index().forNodes( "nodes" );
        registerShutdownHook( graphDb );
        
        fr = new FileReader(INPUT);
        br = new BufferedReader(fr);
        String[] lines = new String[1000];
        String str;
        while((str = br.readLine()) != null){
        	
            int i = 1;
            lines[i-1] = br.readLine();
            while(i < 1000){
            	lines[i] = br.readLine();
            	if(lines[i] == null)
            		break;
            	i++;
            }
        
        
        
        // END SNIPPET: startDb

        // START SNIPPET: transaction
        Transaction tx = graphDb.beginTx();
        
            // Updating operations go here
            // END SNIPPET: transaction
            // START SNIPPET: addData
        	int k = 0;
        try
           {
        	while(k < i){
        		Node firstNode;
        		Node secondNode;
        		Node node1,node2;
        		//System.out.println(lines[k]);
        		 if(lines[k].length() < 3 || lines[k].charAt(0) == '@' ){
        			 k++;
        			 continue;
        		 }
        		 
        		String[] arr = lines[k].split("\t");
        		//System.out.println(lines[k]);
        		//System.out.println(arr[0] + "-" + arr[1] + "->" + arr[2]);
        		
        		node1 = nodeIndex.get( NAME_KEY, arr[0] ).getSingle();
        		if(node1 != null){
        			firstNode = node1;
        		}else{
        			firstNode = graphDb.createNode();
        			firstNode.setProperty( "name", arr[0] );
            		nodeIndex.add( firstNode, NAME_KEY, arr[0] );
        		}
        		
        		
        		node2 = nodeIndex.get( NAME_KEY, arr[2] ).getSingle();
        		if(node2 != null){
        			secondNode = node2;
        		}else{
        			secondNode = graphDb.createNode();
        			secondNode.setProperty( "name", arr[2] );
            		nodeIndex.add( secondNode, NAME_KEY, arr[2] );
        		}
        		//System.out.println(firstNode);
        		//System.out.println(secondNode);

        		relationship = firstNode.createRelationshipTo(secondNode, RelTypes.KNOWS);
        		relationship.setProperty( "rel", arr[1] );
        		// END SNIPPET: addData
        		/*
        		// START SNIPPET: readData
        		System.out.print( firstNode.getProperty( "message" ) );
        		System.out.print( relationship.getProperty( "message" ) );
        		System.out.print( secondNode.getProperty( "message" ) );
        		// END SNIPPET: readData

        		greeting = ( (String) firstNode.getProperty( "message" ) )
                       + ( (String) relationship.getProperty( "message" ) )
                       + ( (String) secondNode.getProperty( "message" ) );

        		// START SNIPPET: transaction
        		 * 
        		 */
        		
        		k++;
        		
        		
        }
        		tx.success();
        		
        	}
        	finally
            {
              tx.finish();
            }
       }
        // END SNIPPET: transaction
        
        //foundNode = nodeIndex.get( NAME_KEY, "1" ).getSingle();
		
		//if(foundNode != null){
		//	System.out.println(foundNode.getProperty(NAME_KEY));
		//}
    }

    private void clearDb()
    {
        try
        {
            FileUtils.deleteRecursively( new File( DB_PATH ) );
        }
        catch ( IOException e )
        {
            throw new RuntimeException( e );
        }
    }
/*
    void removeData()
    {
        Transaction tx = graphDb.beginTx();
        try
        {
            // START SNIPPET: removingData
            // let's remove the data
            firstNode.getSingleRelationship( RelTypes.KNOWS, Direction.OUTGOING ).delete();
            firstNode.delete();
            secondNode.delete();
            // END SNIPPET: removingData

            tx.success();
        }
        finally
        {
            tx.finish();
        }
    }
    */

    void shutDown()
    {
        System.out.println();
        System.out.println( "Shutting down database ..." );
        // START SNIPPET: shutdownServer
        graphDb.shutdown();
        // END SNIPPET: shutdownServer
    }

    // START SNIPPET: shutdownHook
    private static void registerShutdownHook( final GraphDatabaseService graphDb )
    {
        // Registers a shutdown hook for the Neo4j instance so that it
        // shuts down nicely when the VM exits (even if you "Ctrl-C" the
        // running application).
        Runtime.getRuntime().addShutdownHook( new Thread()
        {
            @Override
            public void run()
            {
                graphDb.shutdown();
            }
        } );
    }
    // END SNIPPET: shutdownHook
}